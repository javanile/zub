---
title: zuil
description: WIP GUI framework written in zig
license: MPL-2.0
author: sentrygunlv3
author_github: sentrygunlv3
repository: https://github.com/sentrygunlv3/zuil
keywords:
  - framework
  - gui
  - gui-library
  - retained-mode-gui
date: 2026-05-06
updated_at: 2026-05-06T17:33:27+00:00
last_sync: 2026-05-06T17:33:27Z
package_kind: library
has_library: true
has_binary: false
has_distributable_binary: false
binary_count: 0
distributable_binary_count: 0
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/sentrygunlv3/zuil/
---

<h1 align="center">
<sub>
<img src="./icon.svg" height="36" width="36">
</sub>
ZUIL
</h1>

> [!CAUTION]
> WIP

> [!IMPORTANT]
> NOT TESTED ON WINDOWS\
> the `build.zig` links some libraries as system libraries\
> which i assume doesnt work on windows

---

ZUIL (Zig UI Library)

retained mode gui framework written in zig

using `zglfw`, `zopengl`, `plutosvg`, `harfbuzz` and `freetype` libs

---

<img src="./screenshot.png">

### current features/progress

- asset/file registry
- resource system
- input system (keyboard and mouse only)
- rendering abstraction (shaders are written in GLSL)
- text rendering (WIP)

## examples

### widgets

widgets are created using builder functions

```zig
// .c for common builder functions
widgets.container()
.c.size(.{.dp = 1200}, .{.percentage = 1})
.color(colors.WHITE)
.child(
	widgets.list()
	.c.size(.fill, .fill) // fill is same as .{.percentage = 1}
	.direction(.vertical)
	.spacing(1)
	.children(.{
		widgets.icon()
		.c.size(.{.dp = 200}, .{.dp = 200})
		.c.keepSizeRatio(true)
		.icon("icon.svg")
		.build(),
		widgets.container()
		.c.size(.{.dp = 50}, .{.dp = 30})
		.c.eventCallback(containerClick) // fn (*ZWidget, *const ZEvent) callconv(.c) c_int
		.color(colors.rgb(0, 1.0, 0.5))
		.build(),
		widgets.container()
		.c.size(.{.pixel = 50}, .{.dp = 30})
		.build(),
		widgets.container()
		.c.size(.{.mm = 50}, .{.dp = 30})
		.build(),
		widgets.container()
		.c.size(.{.percentage = 0.5}, .{.dp = 30})
		.build(),
	})
	.build()
)
.build();
```

### test project

there is a test/example project in the `test` directory

keybinds:

- `space`: change the layout
- `F1`: spawn a new window (currently broken see comment in render function inside src/app/window.zig)

## project structure

directories in `src` dir:

- `core` has the base widget system
- `app` has glfw specific things and can be used to create windows that use the core widget system
- `widgets` has the default widgets/shaders
