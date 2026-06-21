USERNAME = "Jaiyansh-4n6"

def generate_svg(contribution_data, total_contributions, generated_at, month_labels,
                 current_streak, longest_streak, active_days,
                 current_start, current_end,
                 longest_start, longest_end):
  position_map = {}
  for item in contribution_data:
      position_map[(item["col"], item["row"])] = item["level"]


# Grid Settings
  x_start = 100
  y_start = 130
  cell    = 16
  gap     = 5
  step    = cell + gap
  cols = max(item["col"] for item in contribution_data) + 1
  rows = 7

  canvas_w = x_start + cols * step + 120
  canvas_h    = 570
  scan_travel = cols * step - cell

  beam_h_top  = y_start - 10
  beam_h_bot  = y_start + (rows - 1) * step + cell + 10
  beam_span   = beam_h_bot - beam_h_top

  # One-way duration in seconds
  one_way_s   = cols * 0.12          # 6.24s
  total_dur_s = one_way_s * 2        # 12.48s full ping-pong cycle

  svg_parts = []

  # ── OPEN + DEFS ───────────────────────────────────────────────────────────────
  svg_parts.append(f'''<svg width="{canvas_w}" height="{canvas_h}" xmlns="http://www.w3.org/2000/svg">

  <defs>

    <filter id="beamGlow" x="-300%" y="-5%" width="700%" height="110%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cellGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-30%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <pattern id="scanPat" x="0" y="0" width="{canvas_w}" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="{canvas_w}" y2="0" stroke="#00ff88" stroke-width="0.6"/>
    </pattern>

    <clipPath id="gridClip">
      <rect x="{x_start - 20}" y="{beam_h_top - 10}"
            width="{scan_travel + cell + 40}"
            height="{beam_span + 20}"/>
    </clipPath>

  </defs>

  <style>
    text {{ font-family: "Consolas", "Courier New", monospace; }}
    .beam-halo {{ animation: haloPulse 0.9s ease-in-out infinite alternate-reverse; }}
    @keyframes haloPulse {{
      from {{ opacity: 0.10; }}
      to   {{ opacity: 0.28; }}
    }}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#070b0f"/>
  <rect width="100%" height="100%" fill="url(#scanPat)" opacity="0.035" pointer-events="none"/>

  ''')

  # ── HEADER ────────────────────────────────────────────────────────────────────
  svg_parts.append('''<!-- Header -->
  <text x="45" y="44" fill="#00ff88" font-size="26" font-weight="bold"
        filter="url(#textGlow)" letter-spacing="3">&gt; CONTRIBUTION GRAPH   </text>
  ''')
  svg_parts.append(
    f'<text x="100" y="80" fill="#9cffc5" font-size="18">'
    f'{total_contributions} contributions in the last year'
    f'</text>'
)
  svg_parts.append(
    f'<text x="100" y="100" fill="#6ddfa8" font-size="12">'
    f'Data Refreshed: {generated_at}'
    f'</text>'
)

  # ── DAY LABELS ────────────────────────────────────────────────────────────────
  days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
  for i, day in enumerate(days):
      svg_parts.append(f'<text x="16" y="{y_start + i*step + 12}" fill="#00ff88" font-size="13" font-weight="bold">{day}</text>\n')

  # ── MONTH LABELS ──────────────────────────────────────────────────────────────
  month_y = y_start - 5
  month_step = cols / max(len(month_labels), 1)
  for i, month in enumerate(month_labels):
    x = x_start + (i * month_step * step)
    svg_parts.append(
        f'<text x="{x}" y="{month_y}" '
        f'fill="#00ff88" '
        f'font-size="13" '
        f'font-weight="bold">  {month}</text>\n'
    )


  # ── CONTRIBUTION GRID WITH SYNCED GLOW ────────────────────────────────────────
  #
  # Timeline (total_dur_s = 12.48s, ping-pong):
  #   0s              → one_way_s (6.24s) : beam travels LEFT → RIGHT
  #   one_way_s       → total_dur_s       : beam travels RIGHT → LEFT
  #
  # For each column col (0..51):
  #   beam_x  = x_start + col * step
  #   Forward pass: beam hits col at t_fwd = (col / (cols-1)) * one_way_s
  #   Reverse pass: beam hits col at t_rev = one_way_s + ((cols-1-col)/(cols-1)) * one_way_s
  #
  # Glow window: ±0.3s around the hit time, clamped to [0, total_dur_s]

  dim_colors = ["#18232c", "#0e2a1a", "#0a3d20", "#134d28", "#1a6632"]
  lit_colors = ["#0d1117", "#26a641", "#39d353", "#57ff7a", "#88ffaa"]

  WINDOW = 0.35   # seconds of glow on each side of beam centre

  svg_parts.append('\n<!-- Contribution grid -->\n')

  for col in range(cols):
      for row in range(rows):
          level = position_map.get((col, row), 0)

          x = x_start + col * step
          y = y_start + row * step

          # Dim base cell (always visible)
          svg_parts.append(
              f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
              f'rx="2" fill="{dim_colors[level]}"/>\n'
          )

          if level == 0:
              continue

          # Compute exact hit times
          frac      = col / (cols - 1)
          t_fwd     = frac * one_way_s
          t_rev     = one_way_s + (1.0 - frac) * one_way_s

          # Build keyTimes + values for a 0→1→0 pulse at each hit
          # We need 6 keyframes: start, pre-fwd, peak-fwd, post-fwd, pre-rev, peak-rev, post-rev, end
          def clamp(v): return max(0.0, min(total_dur_s, v))

          fwd_lo  = clamp(t_fwd - WINDOW)
          fwd_hi  = clamp(t_fwd + WINDOW)
          rev_lo  = clamp(t_rev - WINDOW)
          rev_hi  = clamp(t_rev + WINDOW)

          # Normalise to 0..1 for keyTimes
          D = total_dur_s
          times  = [0.0, fwd_lo/D, t_fwd/D, fwd_hi/D, rev_lo/D, t_rev/D, rev_hi/D, 1.0]
          values = [0,   0,        1,        0,         0,        1,       0,        0  ]

          # Deduplicate adjacent identical times (clamping can cause this)
          clean_t, clean_v = [times[0]], [values[0]]
          for t, v in zip(times[1:], values[1:]):
              if t > clean_t[-1] + 1e-4:
                  clean_t.append(t)
                  clean_v.append(v)

          kt_str = ";".join(f"{t:.4f}" for t in clean_t)
          kv_str = ";".join(str(v)     for v in clean_v)

          svg_parts.append(
              f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
              f'rx="2" fill="{lit_colors[level]}" filter="url(#cellGlow)" opacity="0">\n'
              f'  <animate attributeName="opacity"\n'
              f'           values="{kv_str}" keyTimes="{kt_str}"\n'
              f'           dur="{total_dur_s:.4f}s" repeatCount="indefinite"\n'
              f'           calcMode="linear"/>\n'
              f'</rect>\n'
          )

  # Grid border
  grid_x = x_start - 2
  grid_y = y_start - 2
  grid_w = (cols - 1) * step + cell + 4
  grid_h = (rows - 1) * step + cell + 4
  svg_parts.append(
      f'\n<rect x="{grid_x}" y="{grid_y}" width="{grid_w}" height="{grid_h}" '
      f'rx="3" fill="none" stroke="#1a2a1a" stroke-width="1"/>\n\n'
  )

  # ── SCANNER BEAM (SMIL ping-pong — same timeline as cell glows) ───────────────
  # Using SMIL animateTransform so beam position is on the SAME clock as cell animate
  svg_parts.append(f'''<!-- Scanner beam -->
  <g clip-path="url(#gridClip)">

    <!-- Outer halo -->
    <rect class="beam-halo"
          x="{x_start - 16}" y="{beam_h_top}"
          width="44" height="{beam_span}"
          fill="#00ff88" rx="4"
          filter="url(#beamGlow)">
      <animateTransform attributeName="transform" type="translate"
        values="0,0; {scan_travel},0; 0,0"
        keyTimes="0; 0.5; 1"
        dur="{total_dur_s:.4f}s"
        repeatCount="indefinite"
        calcMode="linear"/>
    </rect>

    <!-- Mid glow -->
    <rect x="{x_start - 7}" y="{beam_h_top}"
          width="22" height="{beam_span}"
          fill="#00ff88" opacity="0.16" rx="2">
      <animateTransform attributeName="transform" type="translate"
        values="0,0; {scan_travel},0; 0,0"
        keyTimes="0; 0.5; 1"
        dur="{total_dur_s:.4f}s"
        repeatCount="indefinite"
        calcMode="linear"/>
    </rect>

    <!-- Core line -->
    <rect x="{x_start}" y="{beam_h_top}"
          width="3" height="{beam_span}"
          fill="#00ff88" opacity="0.95">
      <animateTransform attributeName="transform" type="translate"
        values="0,0; {scan_travel},0; 0,0"
        keyTimes="0; 0.5; 1"
        dur="{total_dur_s:.4f}s"
        repeatCount="indefinite"
        calcMode="linear"/>
    </rect>

    <!-- Top bracket -->
    <path d="M{x_start - 14} {beam_h_top - 8} H{x_start + cell + 6}
            M{x_start - 14} {beam_h_top - 8} V{beam_h_top + 14}
            M{x_start + cell + 6} {beam_h_top - 8} V{beam_h_top + 14}"
          stroke="#65ff65" stroke-width="1.5" fill="none" opacity="0.9">
      <animateTransform attributeName="transform" type="translate"
        values="0,0; {scan_travel},0; 0,0"
        keyTimes="0; 0.5; 1"
        dur="{total_dur_s:.4f}s"
        repeatCount="indefinite"
        calcMode="linear"/>
    </path>

    <!-- Bottom bracket -->
    <path d="M{x_start - 14} {beam_h_bot + 8} H{x_start + cell + 6}
            M{x_start - 14} {beam_h_bot + 8} V{beam_h_bot - 14}
            M{x_start + cell + 6} {beam_h_bot + 8} V{beam_h_bot - 14}"
          stroke="#65ff65" stroke-width="1.5" fill="none" opacity="0.9">
      <animateTransform attributeName="transform" type="translate"
        values="0,0; {scan_travel},0; 0,0"
        keyTimes="0; 0.5; 1"
        dur="{total_dur_s:.4f}s"
        repeatCount="indefinite"
        calcMode="linear"/>
    </path>

  </g>

  ''')

  svg_parts.append(f"""
<text x="100" y="320"
      fill="#00ff88"
      font-size="14">
Status: SCANNING   |   User: {USERNAME}   |   Target: Commits
</text>

""")

  svg_parts.append(f"""
<rect x="450" y="350"
      width="470"
      height="135"
      rx="8"
      fill="#061a2b"
      stroke="#1d4d7a"
      stroke-width="1"/>

<line x1="620" y1="368" x2="620" y2="445"
      stroke="#c58af9" stroke-width="1.5"/>

<line x1="800" y1="368" x2="800" y2="445"
      stroke="#c58af9" stroke-width="1.5"/>

<!-- Active Days -->

<text x="533" y="405"
      fill="#c58af9"
      font-size="24"
      font-weight="bold"
      text-anchor="middle">{active_days}</text>

<text x="540" y="430"
      fill="#c58af9"
      font-size="14"
      text-anchor="middle">Active Days</text>

<text x="540" y="452"
      fill="#7ee8e8"
      font-size="11"
      text-anchor="middle">Last 365 Days</text>

<!-- Current Streak -->

<circle cx="710" cy="402"
        r="35"
        fill="none"
        stroke="#fff4a8"
        stroke-width="4"/>

<text x="710" y="375"
      fill="#fff4a8"
      font-size="22"
      text-anchor="middle">🔥</text>

<text x="710" y="412"
      fill="#fff4a8"
      font-size="24"
      font-weight="bold"
      text-anchor="middle">{current_streak}</text>

<text x="710" y="455"
      fill="#fff4a8"
      font-size="15"
      font-weight="bold"
      text-anchor="middle">Current Streak</text>

<text x="710" y="475"
      fill="#7ee8e8"
      font-size="11"
      text-anchor="middle">{current_start} - {current_end}</text>

<!-- Longest Streak -->

<text x="860" y="405"
      fill="#c58af9"
      font-size="24"
      font-weight="bold"
      text-anchor="middle">{longest_streak}</text>

<text x="860" y="430"
      fill="#c58af9"
      font-size="14"
      text-anchor="middle">Longest Streak</text>

<text x="860" y="452"
      fill="#7ee8e8"
      font-size="11"
      text-anchor="middle">{longest_start} - {longest_end}</text>
  </svg>    
""")
  
  svg_out = "".join(svg_parts)
  return svg_out  

if __name__ == "__main__":
    print("generate_svg.py loaded successfully")

    