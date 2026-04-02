from manim import *
import numpy as np

class HelixScene(ThreeDScene):
    def construct(self):
        R, H = 2, 4
        T_MAX = 2 * PI
        Z_SHIFT = H / 2 

        def helix_func(t):
            return np.array([R * np.cos(t), R * np.sin(t), (H * t / (2 * PI)) - Z_SHIFT])

        title = Text("Длина пространственной кривой", font_size=28).to_edge(UP, buff=0.3)
        
        formula = MathTex(
            r"\vec{r}(t) = \begin{cases} x = R \cos t \\ y = R \sin t \\ z = \frac{Ht}{2\pi} \end{cases}",
            font_size=22
        ).to_corner(UL).shift(DOWN*0.7 + RIGHT*0.2)

        axes = ThreeDAxes()
        helix = ParametricFunction(helix_func, t_range=[0, T_MAX], color=YELLOW, stroke_width=5)
        
        cylinder = Surface(
            lambda u, v: np.array([R * np.cos(u), R * np.sin(u), v - Z_SHIFT]),
            u_range=[0, T_MAX], v_range=[0, H],
            resolution=(32, 16), checkerboard_colors=[BLUE_D, BLUE_E], fill_opacity=0.2
        )

        self.add_fixed_in_frame_mobjects(title, formula)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        self.play(Write(title), FadeIn(formula, shift=RIGHT))
        self.play(Create(axes), Create(cylinder), run_time=2)
        self.play(Create(helix), run_time=3)
        self.wait(1)

        t0, dt = PI * 0.7, 0.6
        p1 = helix_func(t0)
        p2 = helix_func(t0 + dt)
        
        p_x = [p2[0], p1[1], p1[2]]
        p_xy = [p2[0], p2[1], p1[2]]

        dx = Line(p1, p_x, color=RED, stroke_width=10)
        dy = Line(p_x, p_xy, color=GREEN, stroke_width=10)
        dz = Line(p_xy, p2, color=BLUE, stroke_width=10)
        
        box = DashedVMobject(Line(p1, [p1[0], p2[1], p1[2]], color=GRAY).add(Line([p1[0], p2[1], p1[2]], p_xy)))

        pyth_text = MathTex(r"dl = \sqrt{dx^2 + dy^2 + dz^2}", font_size=36, color=YELLOW)
        pyth_bg = BackgroundRectangle(pyth_text, color=BLACK, fill_opacity=0.7, buff=0.1)
        pyth_group = VGroup(pyth_bg, pyth_text).to_corner(UR, buff=0.5)

        self.move_camera(phi=80 * DEGREES, theta=20 * DEGREES, zoom=2.5, frame_center=p1)
        self.play(Create(VGroup(dx, dy, dz, box)), run_time=2)
        self.add_fixed_in_frame_mobjects(pyth_group)
        self.play(FadeIn(pyth_group, shift=LEFT))
        self.wait(3)

        self.play(FadeOut(dx), FadeOut(dy), FadeOut(dz), FadeOut(box), FadeOut(pyth_group), FadeOut(formula))
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, zoom=0.85, frame_center=[0,0,0])

        def get_unroll_surf(alpha):
            return Surface(
                lambda u, v: np.array([
                    interpolate(R * np.cos(u), R * u - R * PI, alpha),
                    interpolate(R * np.sin(u), 0, alpha),
                    v - Z_SHIFT
                ]),
                u_range=[0, T_MAX], v_range=[0, H],
                checkerboard_colors=[BLUE_D, BLUE_E], fill_opacity=0.3
            )

        def get_unroll_helix(alpha):
            return ParametricFunction(
                lambda t: np.array([
                    interpolate(R * np.cos(t), R * t - R * PI, alpha),
                    interpolate(R * np.sin(t), 0, alpha),
                    (H * t / (2 * PI)) - Z_SHIFT
                ]),
                t_range=[0, T_MAX], color=YELLOW, stroke_width=6
            )

        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.play(FadeOut(axes))

        alpha_tracker = ValueTracker(0)
        curr_cyl = cylinder
        curr_hel = helix

        def update_cyl(obj):
            new_surf = get_unroll_surf(alpha_tracker.get_value())
            obj.become(new_surf)

        def update_hel(obj):
            new_hel = get_unroll_helix(alpha_tracker.get_value())
            obj.become(new_hel)

        curr_cyl.add_updater(update_cyl)
        curr_hel.add_updater(update_hel)
        
        self.play(alpha_tracker.animate.set_value(1), run_time=4, rate_func=linear)
        curr_cyl.remove_updater(update_cyl)
        curr_hel.remove_updater(update_hel)
        self.wait(0.5)

        flat_rect = Rectangle(width=2*PI*R, height=H).move_to(ORIGIN)
        
        brace_bottom = Brace(flat_rect, DOWN, buff=0.1)
        label_bottom = MathTex(r"2\pi R", font_size=36).next_to(brace_bottom, DOWN)
        
        brace_right = Brace(flat_rect, RIGHT, buff=0.1)
        label_right = MathTex(r"H", font_size=36).next_to(brace_right, RIGHT)
        
        final_formula = MathTex(r"L = \sqrt{(2\pi R)^2 + H^2}", color=YELLOW, font_size=42).to_edge(UP, buff=1.2)

        labels = VGroup(brace_bottom, label_bottom, brace_right, label_right, final_formula)
        self.add_fixed_in_frame_mobjects(labels)
        
        self.play(Create(brace_bottom), Write(label_bottom))
        self.play(Create(brace_right), Write(label_right))
        self.play(Write(final_formula))
        self.wait(5)