# Blinded AI rating (secondary validation) — prompt and conditions

- Date: 2026-10-26. Rater: two independent instances of Claude Opus 5.5 (Anthropic), run as
  Claude Code sub-agents, each given 13 of the 26 grid images (6 snippets per image, 152 snippets).
- Blinding: the PNG grids were copied to a separate scratch folder that contained no key,
  code or labels. The images show only the 40-s arterial waveform with the 2-s target window
  shaded; snippet IDs are random and carry no stratum information. The rater had a file-read
  tool and was instructed to open only the listed images; compliance was by instruction, not
  enforced by tool restriction.
- The rater sees the waveform only, not the monitor MAP, so it can judge morphology but not
  whether a monitor value was wrong.
- The classifier and this rater come from the same model family that helped design the
  classifier; the rating is therefore not independent validation.

Prompt (identical for both instances except for the image range):

> You are a blinded rater of invasive arterial blood pressure waveform snippets from surgical
> patients (radial arterial line, 500 Hz). This is a research validation exercise; your ratings
> are compared later with an algorithm. Do not try to find any answer key, code or other files —
> read ONLY the PNG images named below. [image paths] Each image has up to 6 panels. Each panel is
> labelled with a snippet ID in the top-left corner and shows 40 s of waveform (x-axis seconds,
> y-axis mmHg). A 2-second window from 0 to 2 s is shaded yellow. Context before and after is
> shown so you can judge it. For every snippet, judge ONLY the yellow 2-s window: rating
> "valid" if the waveform in the yellow window is a faithful, physiological arterial pressure
> trace (including genuine hypotension, arrhythmia, low pulse pressure from real physiology),
> "artefact" if the pressure in that window is not the patient's true arterial pressure, or
> "unsure"; artefact_type (only when artefact): flush, zero, sampling, damping, noise,
> recovery, other; confidence 1–3. Return ONLY a CSV with header
> `snippet,rating,artefact_type,confidence`.
