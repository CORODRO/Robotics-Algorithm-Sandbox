# -*- coding: utf-8 -*-
"""Quintic polynomial trajectory-planning example for smooth path-generation studies."""

import math

import matplotlib.pyplot as plt
import numpy as np

MAX_T = 100.0
MIN_T = 5.0
show_animation = False


class QuinticPolynomial:
    """Quintic polynomial with position, velocity, and acceleration boundary conditions."""

    def __init__(self, xs, vxs, axs, xe, vxe, axe, duration):
        self.a0 = xs
        self.a1 = vxs
        self.a2 = axs / 2.0

        matrix = np.array(
            [
                [duration ** 3, duration ** 4, duration ** 5],
                [3 * duration ** 2, 4 * duration ** 3, 5 * duration ** 4],
                [6 * duration, 12 * duration ** 2, 20 * duration ** 3],
            ]
        )
        values = np.array(
            [
                xe - self.a0 - self.a1 * duration - self.a2 * duration ** 2,
                vxe - self.a1 - 2 * self.a2 * duration,
                axe - 2 * self.a2,
            ]
        )
        x = np.linalg.solve(matrix, values)

        self.a3 = x[0]
        self.a4 = x[1]
        self.a5 = x[2]

    def calc_point(self, t):
        return (
            self.a0
            + self.a1 * t
            + self.a2 * t ** 2
            + self.a3 * t ** 3
            + self.a4 * t ** 4
            + self.a5 * t ** 5
        )

    def calc_first_derivative(self, t):
        return (
            self.a1
            + 2 * self.a2 * t
            + 3 * self.a3 * t ** 2
            + 4 * self.a4 * t ** 3
            + 5 * self.a5 * t ** 4
        )

    def calc_second_derivative(self, t):
        return 2 * self.a2 + 6 * self.a3 * t + 12 * self.a4 * t ** 2 + 20 * self.a5 * t ** 3

    def calc_third_derivative(self, t):
        return 6 * self.a3 + 24 * self.a4 * t + 60 * self.a5 * t ** 2


def quintic_polynomials_planner(
    sx,
    sy,
    syaw,
    sv,
    sa,
    gx,
    gy,
    gyaw,
    gv,
    ga,
    max_accel,
    max_jerk,
    dt,
):
    """Plan a smooth 2D trajectory using quintic polynomials."""

    vxs = sv * math.cos(syaw)
    vys = sv * math.sin(syaw)
    vxg = gv * math.cos(gyaw)
    vyg = gv * math.sin(gyaw)

    axs = sa * math.cos(syaw)
    ays = sa * math.sin(syaw)
    axg = ga * math.cos(gyaw)
    ayg = ga * math.sin(gyaw)

    time = []
    rx = []
    ry = []
    ryaw = []
    rv = []
    ra = []
    rj = []

    for duration in np.arange(MIN_T, MAX_T + MIN_T, MIN_T):
        xqp = QuinticPolynomial(sx, vxs, axs, gx, vxg, axg, duration)
        yqp = QuinticPolynomial(sy, vys, ays, gy, vyg, ayg, duration)

        time = []
        rx = []
        ry = []
        ryaw = []
        rv = []
        ra = []
        rj = []

        for t in np.arange(0.0, duration + dt, dt):
            time.append(t)
            rx.append(xqp.calc_point(t))
            ry.append(yqp.calc_point(t))

            vx = xqp.calc_first_derivative(t)
            vy = yqp.calc_first_derivative(t)
            speed = np.hypot(vx, vy)
            yaw = math.atan2(vy, vx)
            rv.append(speed)
            ryaw.append(yaw)

            ax = xqp.calc_second_derivative(t)
            ay = yqp.calc_second_derivative(t)
            accel = np.hypot(ax, ay)
            if len(rv) >= 2 and rv[-1] - rv[-2] < 0.0:
                accel *= -1
            ra.append(accel)

            jx = xqp.calc_third_derivative(t)
            jy = yqp.calc_third_derivative(t)
            jerk = np.hypot(jx, jy)
            if len(ra) >= 2 and ra[-1] - ra[-2] < 0.0:
                jerk *= -1
            rj.append(jerk)

        if max(abs(value) for value in ra) <= max_accel and max(abs(value) for value in rj) <= max_jerk:
            break

    if show_animation:  # pragma: no cover
        for idx, _ in enumerate(time):
            plt.cla()
            plt.gcf().canvas.mpl_connect(
                "key_release_event",
                lambda event: [exit(0) if event.key == "escape" else None],
            )
            plt.grid(True)
            plt.axis("equal")
            plot_arrow(sx, sy, syaw)
            plot_arrow(gx, gy, gyaw)
            plot_arrow(rx[idx], ry[idx], ryaw[idx])
            plt.title(
                "Time[s]:"
                + str(time[idx])[0:4]
                + " v[m/s]:"
                + str(rv[idx])[0:4]
                + " a[m/ss]:"
                + str(ra[idx])[0:4]
                + " jerk[m/sss]:"
                + str(rj[idx])[0:4]
            )
            plt.pause(0.001)

    return time, rx, ry, ryaw, rv, ra, rj


def plot_arrow(x, y, yaw, length=1.0, width=0.5, fc="r", ec="k"):  # pragma: no cover
    """Plot one or more heading arrows."""
    if not isinstance(x, float):
        for ix, iy, iyaw in zip(x, y, yaw):
            plot_arrow(ix, iy, iyaw)
        return

    plt.arrow(
        x,
        y,
        length * math.cos(yaw),
        length * math.sin(yaw),
        fc=fc,
        ec=ec,
        head_width=width,
        head_length=width,
    )
    plt.plot(x, y)


def main():
    """Run a small trajectory-planning example and optionally plot the results."""
    print(__file__ + " start!!")

    sx = 10.0
    sy = 10.0
    syaw = np.deg2rad(10.0)
    sv = 1.0
    sa = 0.1
    gx = 30.0
    gy = -10.0
    gyaw = np.deg2rad(20.0)
    gv = 1.0
    ga = 0.1
    max_accel = 1.0
    max_jerk = 0.5
    dt = 0.1

    time, x, y, yaw, v, a, j = quintic_polynomials_planner(
        sx, sy, syaw, sv, sa, gx, gy, gyaw, gv, ga, max_accel, max_jerk, dt
    )

    if show_animation:  # pragma: no cover
        plt.plot(x, y, "-r")

        plt.subplots()
        plt.plot(time, [np.rad2deg(value) for value in yaw], "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("Yaw[deg]")
        plt.grid(True)

        plt.subplots()
        plt.plot(time, v, "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("Speed[m/s]")
        plt.grid(True)

        plt.subplots()
        plt.plot(time, a, "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("accel[m/ss]")
        plt.grid(True)

        plt.subplots()
        plt.plot(time, j, "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("jerk[m/sss]")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main()
