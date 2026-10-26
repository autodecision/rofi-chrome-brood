# Chrome Brood for Rofi

A chrome and steel organic frame for an application launcher and list picker.
The artwork is SVG; no Niri, Waybar or Fuzzel installation is required.

## Requirements

- Rofi **2.0.0** is the tested version, with native Wayland support and SVG image loading.
- JetBrains Mono, including its Bold face, for the intended typography.
- Breeze icons (`breeze-dark`) for the intended application icons. You can change
  `icon-theme` in `config.rasi` to an installed icon theme.
- Desktop application entries for application mode. A terminal must be configured
  through Rofi's terminal setting if you launch terminal applications; the package
  does not assume Ghostty is installed. For example, pass `-terminal foot` if using Foot.
- Python 3 **only** if you want to regenerate the bundled artwork.

Package names vary between distributions. Install these through your distribution.

## Try it without replacing your existing configuration

Keep this entire folder together. From this folder:

```sh
chmod +x launch
./launch
printf 'First choice\nSecond choice\n' | ./launch select
```

`launch` works from any current directory and accepts additional Rofi options.
For example: `./launch -terminal foot` or `./launch select -p 'Animations'`.
Application mode starts apps; list mode reads all input before showing and prints
the selected text to stdout. Close stdin after supplying the choices.
Escape cancels. This package does not apply shaders or install Niri animations.

To install, copy the folder to `~/.config/rofi/chrome-brood`, then invoke
`~/.config/rofi/chrome-brood/launch` from your compositor's shortcut or panel.
No installer overwrites your existing Rofi configuration or shortcuts.

Example Niri binding inside `binds { ... }`:

```kdl
Mod+D { spawn-sh "~/.config/rofi/chrome-brood/launch"; }
```

The wrapper sets its working directory so Rofi can find the relative SVG path.
If loading `theme.rasi` from your own configuration, run from this folder or
change the image URL to its installed absolute path. This layout
was designed for `drun` and `dmenu`. Other modes may need layout adjustments.

## Avoiding the image pop-in on Wayland

Stock Rofi 2.0 loads background images and application icons asynchronously,
so the controls can appear before the chrome frame. This is an engine limitation;
changing the theme or adding a shell sleep cannot guarantee a complete first frame.
See the [Rofi 2.0 release notes](https://github.com/davatorium/rofi/releases/tag/2.0.0).

An **optional private build** addresses this for this launcher:

```sh
./build-rofi
./launch
```

The build requires Git, a C compiler, Meson, Ninja, pkg-config, Flex, Bison,
and development files for GLib/GIO/GModule (>=2.72), Cairo, Pango/PangoCairo,
GdkPixbuf, xkbcommon, wayland-client, wayland-cursor, wayland-scanner and
wayland-protocols (>=1.17). SVG support through GdkPixbuf is still required.
Install build dependencies through your distribution before running the script.
The script downloads the pinned upstream Rofi 2.0.0 commit and its submodules,
applies the included patch, and installs only into this folder's `.runtime`.
It builds the Wayland backend; this optional build does not support X11.

`launch` uses this private executable when available and sets
`ROFI_SYNC_THEME_IMAGES=1`. With this opt-in flag, image and icon loading finishes
before each image's first paint. It can increase time until the window appears,
especially with slow icon themes. External thumbnail commands remain asynchronous.
Without the flag, the patched executable retains upstream behavior.

The patch and upstream MIT license are in `patches/`. No prebuilt executable is
included for redistribution. `.runtime` and `.build` are ignored by Git.
Build on the target system; rebuild after moving the folder because the private
build's install prefix is absolute. For rollback, move `.runtime` out of this
folder; `launch` then falls back to the system Rofi (and its loading behavior).
You can select a separately installed private executable with
`ROFI_CHROME_BROOD_BIN=/absolute/path/to/rofi ./launch`.

## Included files

- `theme.rasi`: layout, colors, selection, title and footer.
- `config.rasi`: example application configuration and input behavior.
- `shell.svg`: complete frame, ready to use; contains no external images.
- `assets/carapace.svg`: frame source used by the artwork builder.
- `build-assets.py`: regenerates `shell.svg` with Python's standard library.
- `launch`: application launcher and generic list picker.
- `build-rofi` and `patches/`: optional source build for complete image painting.

Regenerate with `python3 build-assets.py`. No files from the original desktop
configuration are required. Theme changes appear the next time Rofi opens.

## Tested and limitations

Tested with Rofi 2.0.0 on Niri/Wayland at 1920×1080: application search and
launch, list selection, Escape cancellation, SVG rendering, title and footer
alignment. The original integrated animation selector was also tested separately.
The standalone bundle is additionally checked from a relocated directory.
The optional image-loading patch was built and tested on Niri/Wayland: startup
frame captures showed the artwork and application icons in the first visible
application frame; all 16 available upstream tests passed.

The theme has a fixed 560×580 logical-pixel window and forces 96 DPI. Small
screens, different scale factors, font substitutions and long labels can change
spacing or clip content. X11, other compositors, older Rofi releases, accessibility
scaling and other Rofi modes have not been verified. It is not yet a claim of
universal compatibility. The exact appearance requires the fonts and icons above.

## Before publishing

Choose a license for the theme, scripts and artwork, and add a LICENSE file.
No license has been selected on your behalf. The visual inspiration is organic
science-fiction UI rendered in steel; no game assets are needed at runtime.
Review the included SVG sources and their provenance before publishing.
