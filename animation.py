from manim import *
import numpy as np

class HelixScene(ThreeDScene):
    def construct(self):
        # ---параметры ---
        R = 2.0
        h_step = 0.6 # z = h*t
        H_total = h_step * 2 * PI
        T_MAX = 2 * PI
        Z_SHIFT = H_total / 2 # Центрируем цилиндр по вертикали

        def helix_func(t):
            return np.array([R * np.cos(t), R * np.sin(t), (h_step * t) - Z_SHIFT])

        # --- текст ---
        title = Text("Кривые в пространстве: Вариант 8", font_size=28).to_edge(UP, buff=0.3)
        
        formula = MathTex(
            r"L = \int_{\alpha}^{\beta} \sqrt{(x')^2 + (y')^2 + (z')^2} \, dt",
            font_size=24, color=BLUE_B
        ).to_corner(UL).shift(DOWN*0.4)

        helix_eq = MathTex(
            r"\vec{r}(t) = \begin{cases} x = R \cos t \\ y = R \sin t \\ z = ht \end{cases}",
            font_size=22
        ).next_to(formula, DOWN, buff=0.3, aligned_edge=LEFT)

        # --- графика ---
        axes = ThreeDAxes()
        helix = ParametricFunction(helix_func, t_range=[0, T_MAX], color=YELLOW, stroke_width=5)
        cylinder = Surface(
            lambda u, v: np.array([R * np.cos(u), R * np.sin(u), v - Z_SHIFT]),
            u_range=[0, T_MAX], v_range=[0, H_total],
            resolution=(32, 16), checkerboard_colors=[BLUE_D, BLUE_E], fill_opacity=0.25
        )

        # --- построение ---
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(0.5)
        
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes), Create(cylinder), run_time=2)
        
        self.add_fixed_in_frame_mobjects(formula, helix_eq)
        self.play(Write(formula), Write(helix_eq))
        self.play(Create(helix), run_time=3)
        self.wait(1)

        # --- пространственный пифагор ---
        self.play(FadeOut(title), FadeOut(formula), FadeOut(helix_eq))

        t0, dt = PI * 0.75, 0.5
        p1 = helix_func(t0)
        p2 = helix_func(t0 + dt)
        
        p_x = [p2[0], p1[1], p1[2]]
        p_xy = [p2[0], p2[1], p1[2]]

        dx = Line(p1, p_x, color=RED, stroke_width=12)
        dy = Line(p_x, p_xy, color=GREEN, stroke_width=12)
        dz = Line(p_xy, p2, color=BLUE, stroke_width=12)
        
        # пунктир
        box = VGroup(
            DashedLine(p1, [p1[0], p2[1], p1[2]], color=GRAY),
            DashedLine([p1[0], p2[1], p1[2]], p_xy, color=GRAY),
            DashedLine(p_x, [p2[0], p1[1], p2[2]], color=GRAY),
            DashedLine([p2[0], p1[1], p2[2]], p2, color=GRAY)
        )

        pyth_label = MathTex(r"dl = \sqrt{dx^2 + dy^2 + dz^2}", font_size=32, color=YELLOW)
        pyth_bg = BackgroundRectangle(pyth_label, color=BLACK, fill_opacity=0.8, buff=0.1)
        pyth_ui = VGroup(pyth_bg, pyth_label).to_edge(UP, buff=0.5)

        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, zoom=2.5, frame_center=p1)
        self.play(
            cylinder.animate.set_fill(opacity=0.05), 
            Create(VGroup(dx, dy, dz, box))
        )
        self.add_fixed_in_frame_mobjects(pyth_ui)
        self.play(FadeIn(pyth_ui, shift=DOWN))
        self.wait(3)

        self.play(FadeOut(dx, dy, dz, box, pyth_ui))
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, zoom=0.8, frame_center=[0,0,0])

        # --- развертка ---
        def get_unroll_surf(a):
            return Surface(
                lambda u, v: np.array([interpolate(R*np.cos(u), R*u - R*PI, a), interpolate(R*np.sin(u), 0, a), v - Z_SHIFT]),
                u_range=[0, T_MAX], v_range=[0, H_total], checkerboard_colors=[BLUE_D, BLUE_E], fill_opacity=0.35
            )

        def get_unroll_helix(a):
            return ParametricFunction(
                lambda t: np.array([interpolate(R*np.cos(t), R*t - R*PI, a), interpolate(R*np.sin(t), 0, a), (h_step * t) - Z_SHIFT]),
                t_range=[0, T_MAX], color=YELLOW, stroke_width=6
            )

        # переход в 2д
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.play(FadeOut(axes))
        
        val = ValueTracker(0)
        cylinder.add_updater(lambda m: m.become(get_unroll_surf(val.get_value())))
        helix.add_updater(lambda m: m.become(get_unroll_helix(val.get_value())))
        
        self.play(val.animate.set_value(1), run_time=4, rate_func=linear)
        cylinder.clear_updaters()
        helix.clear_updaters()
        self.wait(0.5)

        # метки
        anchor_rect = Rectangle(width=2*PI*R, height=H_total).move_to(ORIGIN)
        
        brace_w = Brace(anchor_rect, DOWN, buff=0.05)
        label_w = MathTex(r"2\pi R", font_size=34).next_to(brace_w, DOWN, buff=0.1)
        
        brace_h = Brace(anchor_rect, RIGHT, buff=0.05)
        label_h = MathTex(r"H = 2\pi h", font_size=34).next_to(brace_h, RIGHT, buff=0.1)
        
        final_res = MathTex(
            r"L = 2\pi \sqrt{R^2 + h^2}", 
            color=YELLOW, font_size=42
        ).to_edge(UP, buff=0.7)

        # группируем
        final_ui = VGroup(brace_w, label_w, brace_h, label_h, final_res)
        self.add_fixed_in_frame_mobjects(final_ui)
        
        self.play(Create(brace_w), Write(label_w))
        self.play(Create(brace_h), Write(label_h))
        self.play(Write(final_res))
        self.wait(5)