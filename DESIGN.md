# GitHub profile — lower section

The existing identity header, landscape animation, about section and social links remain the visual anchor. The lower section is an expressive extension of that rose/mauve identity, with generous separation and readable technology names.

## Composition

- A dedicated AI feature leads the lower section, highlighting OpenAI/OpenRouter experience, multimodal pipelines and MCP agents. Its two capability lanes animate data flow and become vertically stacked on mobile.
- Centered native headings introduce AI, the stack, engineering practices and BrechoDev.
- Desktop stack: a tall languages panel beside two wider frontend/backend panels, followed by paired data/infrastructure panels and a full-width integration diagram.
- Mobile uses dedicated, single-column SVG compositions, with languages in two columns. The breakpoint is 600px; never scale the desktop composition down to a phone.
- Engineering is a connected horizontal diagram on desktop and a vertical diagram on mobile.
- BrechoDev is a linked feature panel, with orbital geometry borrowed from the identity header.
- Full technology and practice descriptions are also available as native selectable text in keyboard-operable `details` sections.

## Palette and type

| Role | Color |
| --- | --- |
| Primary text | `#F5EAF1` |
| Supporting text | `#C0AEBD` |
| Rose / backend and portfolio | `#EBAAC7` |
| Lilac / frontend and infrastructure | `#C5A0DB` |
| Peach / languages and integrations | `#EAC4A8` |
| Muted mint / data and messaging | `#9BC6BD` |
| Base surface | `#1B1721` |
| Border | `#49394E` |

SVG typography inherits the original DejaVu Sans voice, with Arial and sans-serif fallbacks. Graphic headings are 25–28 units, body labels 18–23 on desktop and primarily 23–24 on mobile. Native text follows GitHub's typography and selected theme. Rounded panel corners are 16 units; desktop panel gutters are 24 units. Larger breaks separate different types of content.

## Motion and platform constraints

Connection traces run on an 8-second loop, while the BrechoDev geometry rotates over 32 seconds. Text and logos stay still. All new animations have a `prefers-reduced-motion` alternative; their content stays visible without animation support. Effects live inside self-contained SVG images because a GitHub README cannot run custom JavaScript or page CSS. SVGs cannot observe the hosting page's scroll visibility; animation is limited to small vector elements.

The diagrams illustrate areas of experience, not a specific production deployment. Engineering copy is grounded in the supplied CV. No phone number or other additional contact details were copied from that document.

## Maintenance

Run `python3 scripts/build-profile.py` to regenerate the 14 responsive SVGs. The script uses only Python's standard library and reuses the embedded icon paths from the original `assets/stack-*.svg` files; their upstream sources are recorded in `icon-sources.json`. Keep those original files as source assets. New geometry is authored locally.

`preview.html` is a local, animated rendering of the README with approximate GitHub styling. The published profile remains `README.md` plus `assets/`; no custom CSS from the preview is required. Validate changes at 1000px, 390px and 320px, including opened details and reduced motion.

## AI content evidence

AI copy is grounded in the supplied CV, the user’s stated OpenAI/OpenRouter experience and read-only inspection of `naMoska_AI` and `naMoska_Agent`. The current code uses OpenRouter via an OpenAI-compatible client; the profile describes broader provider experience without implying both gateways currently power those runtimes. Hermes is an integrated runtime, not an agent framework authored from scratch. No accuracy, cost-saving or production-readiness claims are made. Source mapping is in `docs/ai-profile-evidence.md`.
