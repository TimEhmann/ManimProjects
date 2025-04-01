from manim import *
import math
import scipy as sp
import sympy

# --- Helper Function for Taylor Approximation ---
def f_deriv(f, x_val, n):
    x = sympy.symbols('x')
    f_n = f
    for _ in range(n):
        f_n = sympy.diff(f_n, x)
    return float(f_n.subs(x, x_val))

# --- Modify taylor_approx_at_a ---
def taylor_approx_at_a(f, x, a, n_terms):
    """Calculates the Taylor expansion of 1/(1+x^2) around 'a' up to n_terms.
    example Usage:
        x_sym = sympy.symbols('x')
        f_expr = math.log(x_sym)
        func = lambda x: taylor_approx_at_a(f_expr, x, 1, i)
    
    """
    val = 0.0
    a = float(a) # Ensure 'a' is a float
    x = float(x) # Ensure 'x' is a float
    for n in range(n_terms + 1):
        deriv_at_a = f_deriv(f, a, n)
        term = deriv_at_a / math.factorial(n) * (x - a)**n
        # Cap term magnitude to avoid excessive spikes when diverging
        if abs(term) > 100: # Adjust cap as needed
            term = np.sign(term) * 100
        val += term
            
    # Cap the output value
    if abs(val) > 5: # Limit based on axes range
        return np.sign(val) * 5
    return val

X_SYM = sympy.symbols('x')
COS = sympy.cos(X_SYM)


class ComplexRadiusOfConvergence_v2(ThreeDScene): # Use ThreeDScene
    # --- Helper for 3D Surface ---
    def func_3d_abs_1_over_1pz2(self, x, y):
        z = complex(x, y)
        denominator = 1 + z**2
        # Add epsilon to avoid division by zero exactly at poles
        if abs(denominator) < 1e-6:
            return 5 # Return a large, but not infinite, value
        val = abs(1 / denominator)
        # Cap height for visualization
        return min(val, 5) 
    
    # --- Helper Function for Taylor Approximation ---
    def f_deriv(self, x_val, n):
        x = sympy.symbols('x')
        f = 1 / (1 + x**2)
        f_n = f
        for _ in range(n):
            f_n = sympy.diff(f_n, x)
        return float(f_n.subs(x, x_val))

    # --- Modify taylor_approx_at_a ---
    def taylor_approx_at_a(self, x, a, n_terms):
        """Calculates the Taylor expansion of 1/(1+x^2) around 'a' up to n_terms."""
        val = 0.0
        a = float(a) # Ensure 'a' is a float
        x = float(x) # Ensure 'x' is a float
        for n in range(n_terms + 1):
            deriv_at_a = self.f_deriv(a, n)
            term = deriv_at_a / math.factorial(n) * (x - a)**n
            # Cap term magnitude to avoid excessive spikes when diverging
            if abs(term) > 100: # Adjust cap as needed
                term = np.sign(term) * 100
            val += term
                
        # Cap the output value
        if abs(val) > 5: # Limit based on axes range
            return np.sign(val) * 5
        return val
    
    def construct(self):

        # Keep N_TAYLOR_TERMS low if using Sympy! Performance depends heavily on this.
        N_TAYLOR_TERMS = 31 # Using 4 terms as per example taylor_approx_at_a

        # --- Part 0: Initial Setup ---
        main_axes = Axes(
            x_range=[-4.5, 4.5, 1], y_range=[-0.5, 2.0, 0.5],
            x_length=12, y_length=5,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN, buff=0.75)
        main_axes_labels = main_axes.get_axis_labels(x_label="x", y_label="f(x)")

        func = lambda x: 1 / (1 + x**2)
        func_graph = main_axes.plot(func, color=BLUE, x_range=[-4.5, 4.5])

        func_label = MathTex(r"f(x) = \frac{1}{1+x^2}", color=BLUE).to_corner(UR).set_z_index(10)
        self.add_fixed_in_frame_mobjects(func_label)

        approx_graph_dynamic = VMobject().set_z_index(1)
        # **** OPTIMIZATION: Store last 'a' value on the mobject itself ****
        approx_graph_dynamic._last_a_value = None # Initialize

        self.play(
            Create(main_axes), Write(main_axes_labels),
            Create(func_graph),
            run_time=1
        )
        self.wait()

        # --- Part 1: Show ROC & Approximation for a=0 ---
        center_a_val = ValueTracker(0.0)
        center_a_dot_on_graph = Dot(color=YELLOW, radius=0.08).set_z_index(2)
        vertical_line = DashedLine(stroke_width=2, color=YELLOW, stroke_opacity=0.7)
        radius_func = lambda a: np.sqrt(a**2 + 1) # Distance from a to +/- i
        roc_group = VGroup().set_z_index(2) # For brace on x-axis

        # --- Updater for Moving Dot and Line ---
        def dot_line_updater(mob):
             a = center_a_val.get_value()
             # Use try-except for safety, although func(a) is well-behaved here
             try: y_val = func(a)
             except Exception: y_val = 0 # Default to 0 on error
             if not np.isfinite(y_val): y_val = 0 # Handle potential inf/nan
             graph_point = main_axes.c2p(a, y_val)
             center_a_dot_on_graph.move_to(graph_point)
             vertical_line.put_start_and_end_on(graph_point, main_axes.c2p(a, 0))
        # Use a dummy mobject for the updater so it can be added/removed easily
        dummy_updater_mob = Mobject().add_updater(dot_line_updater)
        self.add(dummy_updater_mob) # Add the updater immediately

        # --- OPTIMIZED Updater for Dynamic Approximation Graph ---
        def approx_graph_updater(mob):
             current_a = center_a_val.get_value()
             previous_a = getattr(mob, '_last_a_value', None) # Get previous value

             tolerance = 1e-9 # Tolerance for float comparison

             # **** Check if 'a' has changed significantly ****
             a_has_changed = (previous_a is None) or (abs(current_a - previous_a) > tolerance)

             if a_has_changed:
                  # --- Perform expensive calculation ONLY if 'a' changed ---
                  # print(f"Recalculating graph for a = {current_a}") # Debug output
                  a = current_a # Use current_a for clarity below
                  R = radius_func(a)
                  # Define plot range based on ROC, but clamp to axes limits
                  plot_start = max(a - R - 0.2, main_axes.x_range[0])
                  plot_end = min(a + R + 0.2, main_axes.x_range[1])

                  new_graph_generated = False # Flag to check if graph was made
                  # Ensure plot range is valid
                  if plot_end > plot_start + 0.05: # Need some interval width
                       current_approx_func = lambda x: self.taylor_approx_at_a(x, a, N_TAYLOR_TERMS)
                       # Generate x values within the calculated range
                       x_values = np.linspace(plot_start, plot_end, num=150) # Increased points for smoothness
                       y_values = np.array([current_approx_func(x) for x in x_values])

                       # Filter out non-finite values before plotting
                       valid_indices = np.isfinite(y_values) & (np.abs(y_values) < 10) # Also filter extreme values
                       x_values = x_values[valid_indices]
                       y_values = y_values[valid_indices]

                       # Only plot if we have at least two valid points
                       if len(x_values) > 1:
                            new_graph = main_axes.plot_line_graph(
                                x_values=x_values, y_values=y_values,
                                line_color=ORANGE, stroke_width=3.5,
                                add_vertex_dots=False # Usually false for smooth plots
                            )
                            mob.become(new_graph) # Use become to smoothly update
                            new_graph_generated = True # Mark as successful

                  # If plot range was invalid OR graph generation failed, show an empty graph
                  if not new_graph_generated:
                       mob.become(VMobject()) # Become empty

                  # --- Store the current 'a' value for the next frame ---
                  mob._last_a_value = current_a
             # else: # 'a' hasn't changed, do nothing, mob keeps its previous state
                  # print(f"Skipping graph recalc for a = {current_a}") # Debug output
                  pass

        approx_graph_dynamic.add_updater(approx_graph_updater)

        # --- Updater for ROC Brace (on x-axis) ---
        def roc_brace_updater(mob):
            a = center_a_val.get_value()
            R = radius_func(a)
            start_x = a - R; end_x = a + R
            # Clamp the brace ends to the visible x-axis range
            start_x_clamped = max(start_x, main_axes.x_range[0])
            end_x_clamped = min(end_x, main_axes.x_range[1])

            new_group = VGroup() # Start with an empty group
            # Only create brace if the clamped interval is valid
            if end_x_clamped > start_x_clamped + 0.01:
                # Use BraceBetweenPoints for precision
                new_brace = BraceBetweenPoints(
                    main_axes.c2p(start_x_clamped, 0),
                    main_axes.c2p(end_x_clamped, 0),
                    direction=DOWN, color=RED
                )
                new_text = Tex(f"R = {R:.2f}", font_size=28).next_to(new_brace, DOWN, buff=0.1)
                # Add background for better readability
                bg = BackgroundRectangle(new_text, color=config.background_color, fill_opacity=0.8, buff=0.05)
                new_group.add(bg, new_text, new_brace) # Add brace last so text bg is behind brace tip if needed
            mob.become(new_group) # Update the VGroup content

        roc_group.add_updater(roc_brace_updater)

        # Initial display for a=0
        # Force initial calculation by calling update(0) for each updater
        dummy_updater_mob.update(0)
        approx_graph_dynamic.update(0)
        roc_group.update(0)

        self.play(
            Create(center_a_dot_on_graph), Create(vertical_line),
            Create(approx_graph_dynamic), Create(roc_group), # Use Create for initial appearance
            run_time=1
        )
        self.wait(1)

        puzzle_text = Tex("Approximation (orange) matches near 'a', limited by R", font_size=30).next_to(roc_group, DOWN, buff=0.3)
        self.play(Write(puzzle_text))
        self.wait(2)
        self.play(FadeOut(puzzle_text))
        self.wait(0.5)

        # --- Part 2: Dynamic ROC (Real Axis View) ---
        dynamic_explanation = Tex("Observe how approximation and ROC change with 'a'", font_size=30).to_edge(UP)
        self.add_fixed_in_frame_mobjects(dynamic_explanation)
        self.play(Write(dynamic_explanation))
        self.wait(1)

        # Animate 'a' changing. Updaters handle the rest smoothly.
        self.play(center_a_val.animate.set_value(-2), run_time=3, rate_func=smooth)
        self.wait(0.5) # Pause - graph should NOT recalculate here if a hasn't changed
        self.play(center_a_val.animate.set_value(2), run_time=4, rate_func=smooth)
        self.wait(1) # Pause - graph should NOT recalculate here

        # --- Clear updaters before transition ---
        self.remove(dummy_updater_mob) # Remove the dummy object holding the dot/line updater
        approx_graph_dynamic.clear_updaters()
        roc_group.clear_updaters()

        self.play(FadeOut(dynamic_explanation))
        self.remove_fixed_in_frame_mobjects(dynamic_explanation)
        self.wait(0.5)

        # --- Part 3 & 4: 3D Reveal ---
        reveal_text = Tex("The reason lies in the complex plane!", font_size=36).to_edge(UP)
        self.add_fixed_in_frame_mobjects(reveal_text)
        self.play(Write(reveal_text))
        self.wait(1)

        # Fade out 2D elements
        fade_out_2d = [
            main_axes, main_axes_labels, func_graph, approx_graph_dynamic,
            center_a_dot_on_graph, vertical_line, roc_group
        ]
        # Filter out None just in case, though shouldn't be necessary here
        self.play(*[FadeOut(m) for m in fade_out_2d if m is not None],
                  FadeOut(reveal_text))
        self.remove_fixed_in_frame_mobjects(reveal_text) # Remove after fade out
        self.wait(0.5)

        # --- 3D Axes, Surface, Poles ---
        axes_3d = ThreeDAxes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[0, 5.5, 1],
            x_length=7, y_length=7, z_length=4,
        )
        label_re = Tex("Re(z)", font_size=24).move_to(axes_3d.x_axis.get_end() + 0.4*RIGHT)
        label_im = Tex("Im(z)", font_size=24).move_to(axes_3d.z_axis.get_end() + 0.4*OUT)
        label_abs = Tex("$|f(z)|$", font_size=24).move_to(axes_3d.y_axis.get_top() + 0.4*UP)
        #self.add_fixed_in_frame_mobjects(label_re) no idea how to make it face the camera during rotation
        #self.add_fixed_in_frame_mobjects(label_im) no idea how to make it face the camera during rotation
        self.add_fixed_in_frame_mobjects(label_abs)
        labels_3d_group = VGroup(label_re, label_im, label_abs)

        surface = axes_3d.plot_surface(
            lambda u, v: self.func_3d_abs_1_over_1pz2(u, v), u_range=[-2.5, 2.5], v_range=[-2.5, 2.5],
            resolution=(48, 48), colorscale=[(BLUE, 0), (GREEN, 0.5), (YELLOW, 1.5), (RED, 3)], fill_opacity=0.8
        )
        pole_pos_i = axes_3d.c2p(0, 1, 0); pole_neg_i = axes_3d.c2p(0, -1, 0)
        pole_marker_pos = Dot3D(point=pole_pos_i, color=RED, radius=0.1)
        pole_marker_neg = Dot3D(point=pole_neg_i, color=RED, radius=0.1)
        pole_label_pos = MathTex("+i", color=RED, font_size=30).move_to(pole_marker_pos.get_center() + 0.4*(OUT+RIGHT*0.5+UP*0.5))
        pole_label_neg = MathTex("-i", color=RED, font_size=30).move_to(pole_marker_neg.get_center() + 0.4*(OUT+RIGHT*0.5+DOWN*0.5))
        poles_group = VGroup(pole_marker_pos, pole_marker_neg, pole_label_pos, pole_label_neg)

        self.set_camera_orientation(phi=70 * DEGREES, theta=-110 * DEGREES)
        self.play(Create(axes_3d)); self.play(Write(labels_3d_group)) # Create separately
        self.play(Create(surface), FadeIn(poles_group, scale=0.5), run_time=3)
        singularity_text = Tex("Surface shows singularities at $z = \pm i$", font_size=30).to_corner(UL)
        self.add_fixed_in_frame_mobjects(singularity_text)
        self.play(Write(singularity_text)); self.wait(2)
        self.move_camera(theta=70 * DEGREES, phi=60*DEGREES, run_time=4); self.wait(2)


        # --- Part 5: Return to 2D + Complex Plane View ---
        return_text = Tex("Back to the real axis view...", font_size=30).move_to(singularity_text)
        self.add_fixed_in_frame_mobjects(return_text)

        # *** IMPORTANT: Clear 3D billboard updaters ***
        for label in labels_3d_group: label.clear_updaters()
        pole_label_pos.clear_updaters()
        pole_label_neg.clear_updaters()

        self.play(
            FadeOut(axes_3d), FadeOut(labels_3d_group), FadeOut(surface), FadeOut(poles_group),
            ReplacementTransform(singularity_text, return_text)
        )
        self.wait(1)
        self.play(FadeOut(return_text)) # Fade it out properly
        self.remove_fixed_in_frame_mobjects(singularity_text) # remove old text
        self.remove_fixed_in_frame_mobjects(return_text) # remove new text after it fades

        # Reset camera for 2D view
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        # --- Prepare 2D elements for reappearance ---
        center_a_val.set_value(0) # Reset 'a' value
        # *** ISSUE 2 FIX: Force updaters to run *before* FadeIn ***
        # 1. Re-add updaters
        self.add(dummy_updater_mob) # Handles dot and line
        approx_graph_dynamic._last_a_value = None # Force recalc
        approx_graph_dynamic.add_updater(approx_graph_updater)
        roc_group.add_updater(roc_brace_updater)
        # 2. Force update calculation while elements are still invisible
        dummy_updater_mob.update(0)
        approx_graph_dynamic.update(0) # Calculates graph for a=0
        roc_group.update(0) # Calculates brace for a=0

        # Now FadeIn the elements - they will appear in the correct a=0 state
        self.play(
            FadeIn(main_axes), FadeIn(main_axes_labels), FadeIn(func_graph),
            FadeIn(center_a_dot_on_graph), FadeIn(vertical_line),
            FadeIn(approx_graph_dynamic), # Fades in the pre-calculated a=0 graph
            # FadeIn(roc_group) # We will fade this in later explicitly
            run_time=1.5
        )
        self.wait(0.5)

        # --- Create Complex Plane Subplot (Top Left) ---
        complex_plane = ComplexPlane(
             x_range=[-2.2, 2.2, 1], y_range=[-2.2, 2.2, 1],
             x_length=3.5, y_length=3.5, # Slightly larger
             background_line_style={"stroke_opacity": 0.3, "stroke_width": 1.5}
         ).scale(0.8).to_corner(UL, buff=0.2) # Added buffer

        cp_labels = VGroup(
            Tex("Re",font_size=20).next_to(complex_plane.x_axis,DR,buff=0.1),
            Tex("Im",font_size=20).next_to(complex_plane.y_axis,UR,buff=0.1)
        )
        # Poles at +i (0,1) and -i (0,-1) in complex plane
        pole_cp_pos_pt = complex_plane.n2p(1j)
        pole_cp_neg_pt = complex_plane.n2p(-1j)
        pole_cp_pos = Dot(pole_cp_pos_pt, color=RED, radius=0.05)
        pole_cp_neg = Dot(pole_cp_neg_pt, color=RED, radius=0.05)
        pole_cp_label_pos = MathTex("+i", color=RED, font_size=20).next_to(pole_cp_pos, UR, buff=0.05)
        pole_cp_label_neg = MathTex("-i", color=RED, font_size=20).next_to(pole_cp_neg, DR, buff=0.05)
        cp_poles_group = VGroup(pole_cp_pos, pole_cp_neg, pole_cp_label_pos, pole_cp_label_neg)

        # Dot representing 'a' on the real axis of the complex plane
        a_dot_cp = Dot(color=YELLOW, radius=0.05).set_z_index(1)
        a_dot_cp.add_updater(lambda m: m.move_to(complex_plane.n2p(complex(center_a_val.get_value(), 0))))
        a_label_cp = MathTex("a", color=YELLOW, font_size=20)
        a_label_cp.add_updater(lambda m: m.next_to(a_dot_cp, DOWN, buff=0.1))

        # Line from 'a' to nearest singularity (let's choose +i)
        dist_line = Line(color=YELLOW, stroke_width=2, stroke_opacity=0.8).set_z_index(0)
        dist_line.add_updater(lambda m: m.put_start_and_end_on(
            a_dot_cp.get_center(), # Use dot's current center
            pole_cp_pos_pt # Fixed point for +i
        ))

        # Updater for Distance Brace/Text in Complex Plane
        dist_display_group_cp = VGroup().set_z_index(2) # Ensure it's on top
        def dist_updater_cp(mob):
            a = center_a_val.get_value()
            R = radius_func(a) # This is sqrt(a^2 + 1)
            start_pt = dist_line.get_start()
            end_pt = dist_line.get_end()
            new_group = VGroup()
            # Only draw if line has significant length
            if np.linalg.norm(end_pt - start_pt) > 0.02:
                 line_vec = end_pt - start_pt
                 # Calculate perpendicular vector pointing away from origin (usually)
                 perp_vec = normalize(np.array([-line_vec[1], line_vec[0], 0]))
                 mid_point = dist_line.get_center()
                 origin_vec = mid_point - complex_plane.get_origin()
                 # Ensure brace points outwards from origin if origin is not between start/end
                 if abs(np.linalg.norm(origin_vec)) > 1e-6 and np.dot(perp_vec, origin_vec) < 0:
                     perp_vec *= -1
                 # Create brace along the line
                 new_brace = Brace(dist_line, direction=perp_vec, color=YELLOW, sharpness=0.7, buff=0.05)
                 new_text = Tex(f"R = {R:.2f}", font_size=24).next_to(new_brace, perp_vec, buff=0.05) # Smaller font
                 bg = BackgroundRectangle(new_text, color=config.background_color, fill_opacity=0.8, buff=0.05)
                 new_group.add(bg, new_text, new_brace) # Brace last
            mob.become(new_group)

        dist_display_group_cp.add_updater(dist_updater_cp)

        # --- Animate creation of subplot elements ---
        # Add updaters *before* animating creation
        a_dot_cp.update(0)
        a_label_cp.update(0)
        dist_line.update(0)
        dist_display_group_cp.update(0) # Calculate initial state

        self.play(
            FadeIn(complex_plane), Write(cp_labels), FadeIn(cp_poles_group),
            FadeIn(a_dot_cp), Write(a_label_cp), FadeIn(dist_line),
            # *** ISSUE 3 FIX: Use Create or Write for the group ***
            run_time=1.5
        )
        self.play(FadeIn(dist_display_group_cp))
        self.wait(1)

        # Display main ROC brace again
        # It was updated off-screen before, now just FadeIn
        # *** ISSUE 4 FIX: Use FadeIn without self.add beforehand ***
        self.play(FadeIn(roc_group))
        self.wait(1)

        # Run the animation again, with complex plane visualization
        final_explanation = Tex("ROC = Distance from 'a' to nearest singularity $(\pm i)$", font_size=30).to_edge(UP)
        self.add_fixed_in_frame_mobjects(final_explanation)
        self.play(Write(final_explanation))
        self.wait(0.5)

        self.play(center_a_val.animate.set_value(-2), run_time=3, rate_func=smooth)
        self.wait(0.5) # Pause
        self.play(center_a_val.animate.set_value(2), run_time=4, rate_func=smooth)
        self.wait(2) # Pause

        # --- Cleanup updaters before final slide ---
        self.remove(dummy_updater_mob)
        approx_graph_dynamic.clear_updaters()
        roc_group.clear_updaters()
        a_dot_cp.clear_updaters()
        a_label_cp.clear_updaters()
        dist_line.clear_updaters()
        dist_display_group_cp.clear_updaters()
        # Note: 3D billboard updaters were already cleared

        self.wait(1)

        # --- Final Conclusion Slide ---
        # Group all elements currently on screen to fade them out
        elements_to_fade = VGroup(
            main_axes, main_axes_labels, func_graph, center_a_dot_on_graph, vertical_line,
            complex_plane, cp_labels, cp_poles_group, a_dot_cp, a_label_cp, dist_line,
            roc_group, dist_display_group_cp, approx_graph_dynamic
        )
        # Manim handles fading out VGroups containing other mobjects
        self.play(
            FadeOut(elements_to_fade),
            FadeOut(final_explanation),
            FadeOut(func_label) # Fade out fixed mobjects
        )
        # Remove fixed mobjects after they are faded
        self.remove_fixed_in_frame_mobjects(final_explanation, func_label)
        self.wait(1)

        # Conclusion Text
        conclusion_line1 = Tex("The Radius of Convergence (ROC) of a Taylor series")
        conclusion_line2 = Tex(r"centered at '$a$' is the distance from '$a$' to the")
        conclusion_line3 = Tex(r"\textbf{nearest singularity} of the function")
        conclusion_line4 = Tex(r"in the \textbf{complex plane}.")
        conclusion_group = VGroup(conclusion_line1, conclusion_line2, conclusion_line3, conclusion_line4).arrange(DOWN, buff=0.3).scale(0.9)

        caveat_text = Tex(r"*Applies to functions analytic around '$a$'. If no finite singularities exist (entire functions), ROC = $\infty$.", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.3)

        self.play(Write(conclusion_group))
        self.wait(1.5)
        self.play(FadeIn(caveat_text, shift=UP*0.2))
        self.wait(8)
