---
title: zig-goome
description: goome for Zig, a zig package that builds goome.h with zig cc
license: GPL-3.0
author: goome-ui
author_github: goome-ui
repository: https://github.com/goome-ui/zig-goome
keywords:
  - cross-platform
  - gamedev
  - goome
  - gui
  - immediate-mode-gui
  - overlay
  - ui
date: 2026-11-16
category: game-development
updated_at: 2026-11-16T22:44:12+00:00
last_sync: 2026-11-16T22:44:12Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/goome-ui/zig-goome/
---

<p align="center">
  <img src="https://raw.githubusercontent.com/goome-ui/.github/main/profile/logo.png" alt="goome" width="150">
</p>

<h1 align="center">⚡ zig-goome ⚡</h1>

<p align="center">
<b>Overlays on top of everything, normal desktop apps, or ui inside your game, straight from Zig.</b>
</p>

<p align="center">
  <img src="https://goome.wtf/badges/zig-0152.svg" alt="Zig 0.15.2">
  <img src="https://goome.wtf/badges/zig-package.svg" alt="zig fetch, build.zig.zon">
  <img src="https://goome.wtf/badges/dependencies-none.svg" alt="no dependencies">
  <img src="https://img.shields.io/badge/Linux-X11%20%2B%20Wayland-1b1d22?style=flat-square&logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/Windows-10%20%2F%2011-1b1d22?style=flat-square&logo=windows11&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/macOS-14%2B-1b1d22?style=flat-square&logo=apple&logoColor=white" alt="macOS">
  <img src="https://img.shields.io/badge/license-GPL--3.0-1b1d22?style=flat-square" alt="GPL-3.0">
</p>

<p align="center">
  <a href="https://goome.wtf/docs/">Docs</a> &nbsp;·&nbsp;
  <a href="https://goome.wtf/builder/">Builder</a> &nbsp;·&nbsp;
  <a href="https://github.com/goome-ui/examples">Examples</a> &nbsp;·&nbsp;
  <a href="https://github.com/goome-ui/c-goome">C</a> &nbsp;·&nbsp;
  <a href="https://github.com/goome-ui/csharp-goome">C#</a> &nbsp;·&nbsp;
  <a href="https://github.com/goome-ui/python-goome">Python</a> &nbsp;·&nbsp;
  <a href="https://github.com/goome-ui/java-goome">Java</a> &nbsp;·&nbsp;
  <a href="https://github.com/goome-ui/godot-goome">Godot</a> &nbsp;·&nbsp;
  <a href="https://github.com/goome-ui/go-goome">Go</a> &nbsp;·&nbsp;
  <a href="https://github.com/goome-ui/lua-goome">Lua</a>
</p>

<p align="center">
  Questions go in <a href="https://github.com/goome-ui/c-goome/discussions">Discussions</a>. If you want to help, the <a href="https://github.com/goome-ui/zig-goome/labels/good%20first%20issue">good first issues</a> are small ones to start with.
</p>

<p align="center">
  This is <a href="https://github.com/goome-ui/c-goome">goome</a> for Zig. Draw over the whole screen and clicks only stop where you drew something.<br>
  It does app windows and offscreen frames for game engines too. build.zig compiles goome.h with zig's own C compiler, so theres nothing else to install, not even on Windows.<br>
  The wrapper is thin on purpose. Everything from goome.h is still there as <code>goome.c</code> if you want the raw C.<br> <br>
  Do you like this project? If so, please let me know!
  <a href="https://sevvy-wevvy.com/discord">Discord</a>
</p>

<h3 align="center">🫥 An overlay on top of everything 🫥</h3>

```zig
const goome = @import("goome");

pub fn main() !void {
    const g = try goome.Goome.open(.{ .title = "my overlay" });
    defer g.deinit();
    while (true) {
        while (try g.poll(16)) |ev| {
            if (ev.kind == .quit) return;
        }
        const c = g.begin(0) orelse continue;
        c.roundRect(100, 100, 220, 60, 12, 0xE0202838);
        _ = c.text(118, 120, "im on top of everything", false, 0xFFFFFFFF);
        try g.end(c, &.{goome.rect(100, 100, 220, 60)});
    }
}
```

<h3 align="center">🪟 A normal app 🪟</h3>

```zig
const g = try goome.Goome.openApp("My app", 960, 640);
defer g.deinit();
const ui = try g.ui();
defer ui.deinit();
var name: [64]u8 = [_]u8{0} ** 64;
while (true) {
    while (try g.poll(16)) |ev| {
        if (ev.kind == .quit or ev.kind == .close) return;
        _ = ui.feed(ev);
    }
    _ = ui.begin(0) orelse continue;
    if (ui.app("My app", 0)) {
        _ = ui.input("Name", &name);
        if (ui.button("Say hi")) ui.toast("hi", 2000);
    }
    ui.appEnd();
    ui.end();
}
```

<h3 align="center">🎮 Inside a game engine 🎮</h3>

```zig
const g = try goome.Goome.openOffscreen(800, 600, 1);
defer g.deinit();
const ui = try g.ui();
defer ui.deinit();
var win: goome.Window = .{ .x = 20, .y = 20, .w = 260 };
var volume: f64 = 0.5;
while (running) {
    try g.push(.{ .kind = .motion, .x = mouse_x, .y = mouse_y });  // your engines input goes in
    while (try g.poll(0)) |ev| _ = ui.feed(ev);
    _ = ui.begin(0) orelse continue;
    if (ui.window("Settings", &win, goome.win.move)) _ = ui.slider("Volume", &volume, 0, 1, null);
    ui.windowEnd();
    ui.end();
    const frame = try g.frame();                                   // premultiplied BGRA pixels come out
    uploadTexture(frame.pixels(), frame.width(), frame.height());
}
```

<p align="center">
Overlay is still the default, nothing changes unless you ask for an app or offscreen.<br>
Zig can also go inside a game for mods, link the static <code>goome</code> lib from this package into your hook dll. <a href="https://github.com/goome-ui/c-goome">c-goome</a> has the DirectX 9/11/12 and Vulkan backends plus Metal and GL that you call through <code>goome.c</code>.
</p>

<details>
<summary align="center"><b>⬇️ Install ⬇️</b></summary>

<br>

<p align="center">
You need <a href="https://ziglang.org/download/">Zig 0.15.2</a>. In your project:
</p>

```sh
zig fetch --save git+https://github.com/goome-ui/zig-goome#dev
```

<p align="center">
Then in your <code>build.zig</code>:
</p>

```zig
const goome = b.dependency("goome", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("goome", goome.module("goome"));
```

<p align="center">
Thats it, the module brings goome's C with it and links libc. Nothing gets linked on top of that on any OS, goome loads what it needs at runtime.<br> <br>
For a version tag instead of dev put it after the <code>#</code>, like <code>#v0.5.6</code>. If you only want the C side, <code>goome.artifact("goome")</code> is a static lib with <code>goome.h</code> installed next to it.
</p>

<p align="center">
Working from a clone:
</p>

```sh
git clone https://github.com/goome-ui/zig-goome
cd zig-goome
zig build test            # all the tests, on the test backend
zig build examples        # zig-out/bin/hello, grab, ui_demo, anim, text
zig build run-ui_demo
```
</details>

<details>
<summary align="center"><b>🚀 Quick Start 🚀</b></summary>

<br>

<p align="center">
A whole overlay that draws a box and prints clicks on it:
</p>

```zig
const std = @import("std");
const goome = @import("goome");

pub fn main() !void {
    const g = try goome.Goome.open(.{ .title = "my overlay" });
    defer g.deinit();
    var pace: goome.Pacer = .{};
    while (true) {
        while (try g.poll(pace.wait(60))) |ev| {
            switch (ev.kind) {
                .quit => return,
                .down => std.debug.print("clicked at {d:.0},{d:.0}\n", .{ ev.x, ev.y }),
                else => {},
            }
        }
        const c = g.begin(0) orelse continue;  // null when theres nothing to draw on
        c.roundRect(100, 100, 200, 80, 12, 0xE0202838);
        _ = c.text(116, 128, "click me", true, 0xFFFFFFFF);
        try g.end(c, &.{goome.rect(100, 100, 200, 80)});  // only this part takes clicks
    }
}
```

<p align="center">
Colors are plain <code>0xAARRGGBB</code> u32s and every position is in logical desktop coords, same as in C.<br>
Every goome error code is a Zig error (<code>error.NotSupported</code>, <code>error.Again</code>, <code>error.NoDisplay</code>...), so <code>try</code> and <code>catch</code> work like you'd expect. <code>goome.errorCode(e)</code> turns one back into the C number.
</p>
</details>

<details>
<summary align="center"><b>🎛️ UI Kit 🎛️</b></summary>

<br>

<p align="center">
The immediate mode ui works like in C. Widgets take a pointer to your value and return true when they changed it this frame. You keep your own variables and call the widgets every frame.
</p>

```zig
const ui = try g.ui();
defer ui.deinit();
var win: goome.Window = .{ .x = 40, .y = 40, .w = 300 };  // h 0 = fit the content
var logo = try goome.Bitmap.load("logo.png");
defer logo.deinit();
var volume: f64 = 0.5;
var muted = false;
var name: [64]u8 = undefined;
goome.setText(&name, "goome");

_ = ui.begin(0) orelse continue;
if (ui.window("Settings", &win, goome.win.move | goome.win.collapse)) {
    ui.image(&logo, 64, 64, 12);
    if (ui.button("Say hi")) std.debug.print("hi\n", .{});
    _ = ui.slider("Volume", &volume, 0, 1, "%.2f");
    _ = ui.toggle("Muted", &muted);
    _ = ui.input("Name", &name);
    ui.labelFmt("hi {s}", .{goome.text(&name)});
}
ui.windowEnd();
ui.end();
```

<p align="center">
Checkboxes and toggles take a <code>*bool</code>, radios, combos, tabs and int sliders an <code>*i32</code>, text boxes a <code>[]u8</code> buffer with the text null terminated inside it (<code>goome.text(&buf)</code> reads it, <code>goome.setText(&buf, "x")</code> writes it).<br>
<code>goome.Window</code> keeps a windows spot and size between frames and if its open. It has to live as long as the window does, goome holds on to it until <code>windowEnd</code>. <code>win.setOpen(false)</code> hides it, <code>goome.win.close</code> gives it an x that does the same.<br>
<code>ui.label(text)</code> never treats your text as a format string. <code>ui.labelFmt("{d} fps", .{fps})</code> formats it the Zig way.<br> <br>
The begin and end pairs are the same as C: <code>window</code> / <code>windowEnd</code>, <code>scrollBegin</code> / <code>scrollEnd</code>, <code>app</code> / <code>appEnd</code>, <code>tableBegin</code> / <code>tableEnd</code> and <code>splitBegin</code> / <code>splitEnd</code> always get their end. <code>menubarBegin</code>, <code>menuBegin</code>, <code>contextBegin</code>, <code>popupBegin</code>, <code>modalBegin</code> and <code>tree</code> only get one when they returned true.
</p>

```zig
if (ui.tableBegin("files", 3, 200, goome.c.GOOME_TABLE_SORTABLE | goome.c.GOOME_TABLE_STRIPES)) {
    ui.tableColumn("Name", 0);
    ui.tableColumn("Size", 80);
    ui.tableColumn("Kind", 0);
    _ = ui.tableSort(&sort_col, &sort_desc);
    for (files) |f| {
        ui.tableRow();
        ui.label(f.name);
        ui.tableNext();
        ui.labelFmt("{d}", .{f.size});
        ui.tableNext();
        ui.label(f.kind);
    }
}
ui.tableEnd();

if (ui.splitBegin("main", false, &side)) {
    ui.label("left");
    ui.splitNext();
    _ = ui.textEdit("body", &body, 0, goome.c.GOOME_EDIT_LINE_NUMBERS | goome.c.GOOME_EDIT_WRAP);
}
ui.splitEnd();

_ = ui.scrollBegin("log", 200);
const rows = ui.listClip(lines.len, 0);   // only the rows you can see
for (rows.first..rows.last) |i| ui.label(lines[i]);
ui.scrollEnd();

ui.plotLines("fps", fps_history, 0, 144, 60);
_ = ui.dragFloat("Speed", &speed, 0.1, 0, 10, null);
if (ui.link("open the docs")) {}
ui.toast("saved", 2000);
```

<p align="center">
<code>ui.theme()</code> is the real <code>goome_theme</code>, so every color and size is a field (<code>ui.theme().accent = 0xFF6FDC5F</code>). <code>themeDark</code>, <code>themeLight</code>, <code>themeMake(accent, dark, radius)</code> and <code>themePreset</code> are on the ui, the style stack is <code>pushColor</code> / <code>pushNum</code> / <code>pushRadii</code> / <code>pushFont</code> / <code>pushSkin</code> / <code>pushTheme</code> / <code>pushIcon</code> and <code>pop(n)</code>.<br>
<code>ui.custom(id, w, h, flags, &item)</code> plus <code>ui.canvas()</code> draws whole new widgets, <code>ui.store(id, n)</code> keeps a few f64s per widget between frames.
</p>
</details>

<details>
<summary align="center"><b>🎞️ Animations 🎞️</b></summary>

<br>

<p align="center">
<code>ui.anim(id, target, ms, ease)</code> gives you a number that slides to the target, call it every frame with whatever the target is right now. goome keeps where it was per id and keeps <code>ui.animating()</code> true while something is still moving, so you know to keep drawing.
</p>

```zig
const x = ui.anim("box", if (open) 200 else 10, 160, .out);
const glow = ui.animColor("glow", if (hovered) 0xFF6FDC5F else 0x00000000, 200, .linear);
const wobble = goome.ease(.spring, 0.5);   // just the curve, t 0..1
```

<p align="center">
The eases are <code>goome.Ease</code>: <code>.linear</code>, <code>.in</code>, <code>.out</code>, <code>.in_out</code>, <code>.smooth</code>, <code>.back</code>, <code>.spring</code> and <code>.bounce</code> (spring and bounce go a bit past the end and come back).
</p>
</details>

<details>
<summary align="center"><b>🌍 Emoji, RTL And Typing 🌍</b></summary>

<br>

<p align="center">
Color emoji, Arabic and Hebrew just work in every text call and widget. <code>Font.system</code> already adds your systems emoji font, for a font you loaded yourself add one with <code>font.fallback(emoji)</code>. The font doesnt own the fallback, so keep it around until you <code>deinit</code> the first one.<br>
<code>goome.textDir(.rtl)</code> sets the paragraph direction for all text, <code>.auto</code> (the default) picks it from the first real letter of each line.
</p>

```zig
const emoji = try goome.Font.load("NotoColorEmoji.ttf");
defer emoji.deinit();
font.fallback(emoji);
goome.textDir(.rtl);
_ = c.fontText(font, 20, 10, 10, "שלום 👋 مرحبا", 0xFFFFFFFF);
goome.textDir(.auto);
```

<p align="center">
Inputs and text edits turn the IME on by themselves while they have focus, so Japanese, Chinese, Korean and dead keys work without you doing anything. If you draw your own text box, <code>g.textInput(true, caret_rect)</code> turns it on and you get <code>.text</code> and <code>.preedit</code> events. <code>g.eventText()</code> has all of the text (the event itself cuts at 63 bytes) and <code>g.preeditCursor()</code> is where the caret is in it.
</p>
</details>

<details>
<summary align="center"><b>♿ Screen Readers ♿</b></summary>

<br>

<p align="center">
The ui kit tells screen readers about every widget, on by default for app windows. <code>ui.a11yOn(true)</code> turns it on for overlays and offscreen too.<br>
For your own <code>ui.custom</code> widgets, say what they are right before them:
</p>

```zig
ui.a11yRole(.slider, "Volume knob");
ui.a11yValue("11");
_ = ui.custom("knob", 40, 40, 0, &item);
```

<p align="center">
In a game engine you can read the whole tree and hand it to your own a11y layer. <code>parent</code> is an index into <code>nodes</code> (or null), <code>label</code> and <code>value</code> are slices:
</p>

```zig
var tree = try ui.a11yTree(allocator);
defer tree.deinit();
for (tree.nodes) |n| std.debug.print("{s} {s} {s}\n", .{ @tagName(n.role), n.label, n.value });
if (tree.find(.button, "OK")) |i| std.debug.print("ok is at {d},{d}\n", .{ tree.nodes[i].x, tree.nodes[i].y });
```
</details>

<details>
<summary align="center"><b>📚 The API 📚</b></summary>

<br>

<p align="center">
Everything from <a href="https://github.com/goome-ui/c-goome/blob/main/include/goome.h">goome.h</a> is in here. <a href="https://goome.wtf/docs/">The docs</a> explain every part of it. The names are the C ones without <code>goome_</code>, in camelCase, and hang off the type they work on.
</p>

| | |
|:--|:--|
| `goome.Goome.open(.{...})` / `openApp` / `openOffscreen` | gives you a `*Goome`, `deinit()` closes it. `Options` has every `goome_opts` field with Zig types |
| `g.poll(ms)` | `?Event`, so `while (try g.poll(16)) \|ev\|` drains the queue. `ev.kind` is an enum, `ev.typed()` and `ev.message()` are slices |
| `g.monitors(&buf)` | fills your array, gives back the part it used |
| `g.capture(mon, rect)` | an `Image`, `.pixels()` is a `[]u32` straight over goomes buffer, good until the next grab of that monitor |
| `g.begin(mon)` / `g.end(canvas, &hits)` | a frame, hits are `[]const Rect` |
| `g.hotkey("alt+h", 1)`, `g.keyboard(true)`, `g.grab(true)`, `g.pointer()` | input |
| `g.controlPath()`, `goome.send(dir, msg)` | the control fifo |
| `g.setTitle`, `setSize`, `setPosition`, `setState`, `drag`, `show`, `setCursor`, `clipboard`, `setClipboard`, `dropPath` | app windows |
| `g.push(ev)`, `pushClick`, `frame()`, `frameDirty()`, `frameCopy(buf, stride, .rgba, rect)`, `hit(x, y)`, `resize` | offscreen |
| `goome.Bitmap.load` / `loadMem` / `fromArgb` / `wrap` | `deinit()` frees it, twice is fine |
| `goome.Font.load` / `loadIndex` / `loadMem` / `system` | `measure`, `width`, `lineHeight`, `fallback`, `deinit()` |
| `ui.anim`, `ui.animColor`, `goome.ease`, `goome.textDir` | animations and text direction |
| `g.textInput`, `g.eventText`, `g.preeditCursor` | IME |
| `ui.a11yOn`, `a11yRole`, `a11yValue`, `a11yTree(allocator)` | screen readers, `ui.a11yRaw(&buf)` fills raw C nodes without allocating |
| `goome.parseCombo`, `goome.Pacer`, `goome.nowMs`, `goome.savePpm` | the small stuff |
| `goome.c` | the whole raw header from `@cImport`, every `GOOME_` constant lives there |

<p align="center">
The constants you use all the time have short names: <code>goome.key.esc</code>, <code>goome.mod.ctrl</code>, <code>goome.cap.hotkeys</code>, <code>goome.win.move</code>, <code>goome.want.mouse</code>, <code>goome.window_flags.borderless</code>. Everything else is <code>goome.c.GOOME_*</code>.<br>
<code>canvas.raw()</code>, <code>ui.raw()</code>, <code>image.raw</code> and <code>bitmap.raw</code> hand you the C struct if you need a field the wrapper doesnt show.
</p>
</details>

<details>
<summary align="center"><b>🎨 Drawing 🎨</b></summary>

<br>

<p align="center">
The canvas methods are the C draw functions without the <code>goome_draw_</code> part:
</p>

```zig
c.rect(x, y, w, h, color);
c.rrect(x, y, w, h, goome.radius(12), color);
c.rrect(x, y, w, h, goome.corners(4, 20, 0, 33), color);   // tl tr br bl
c.rrectGrad(x, y, w, h, goome.radius(12), top, bottom, false);
c.shadow(x, y, w, h, radius, blur, color);
c.circle(cx, cy, r, color);
c.ring(cx, cy, r, width, color);
c.arc(cx, cy, r, width, a0, a1, color);
c.poly(&.{ .{ 80, 5 }, .{ 98, 85 }, .{ 40, 35 } }, color);
c.line(x0, y0, x1, y1, width, color);
c.frame(x, y, w, h, width, color);
c.bitmap(&bmp, x, y, w, h, goome.radius(0), 0xFFFFFFFF);
_ = c.text(x, y, "built in font", true, color);
_ = c.fontText(font, 20, x, y, "real font", color);
c.clipPush(20, 15, 80, 50);
c.clipPop();
```

<p align="center">
<code>c.pixels()</code> is a <code>[]u32</code> right over goomes buffer (premultiplied ARGB, <code>c.stride()</code> per row), nothing gets copied. Write into it and call <code>c.damage(rect)</code>.<br>
<code>goome.OwnedCanvas.init(allocator, w, h, stride, scale)</code> makes a canvas on your own memory, for drawing offscreen and blitting with <code>c.blit(other.canvas(), alpha, dx, dy)</code>.
</p>
</details>

<details>
<summary align="center"><b>🧩 Examples 🧩</b></summary>

<br>

- `examples/hello.zig` - a box you can click and type into, alt+h hides it, esc or the x quits
- `examples/grab.zig` - `zig build run-grab -- [monitor] [x y w h] out.ppm` saves a screen grab
- `examples/ui_demo.zig` - the ui kit demo with every widget, a theme editor and a stats window
- `examples/anim.zig` - every ease side by side, a color fade, a springy toggle and a bouncing badge
- `examples/text.zig` - emoji, Arabic and Hebrew in labels and text boxes with a direction switch. `zig build run-text -- out.ppm` renders it offscreen to a file and prints what a screen reader sees

They're ports of the C examples and do the same thing. `tests/consumer` is a tiny project that pulls this repo in as a package, CI builds it to make sure that keeps working.<br>
Way more small projects live in [goome-ui/examples](https://github.com/goome-ui/examples).

```sh
zig build run-ui_demo
```
</details>

<details>
<summary align="center"><b>🖥️ Where It Works 🖥️</b></summary>

<br>

Linux (X11 and Wayland), Windows 10 / 11 and macOS 14+, same as goome. Not every desktop can do everything, the <a href="https://github.com/goome-ui/c-goome#readme">c-goome README</a> has the table and <code>g.can(goome.cap.hotkeys)</code> tells you at runtime.

On Mac stay on the main thread.
</details>

<details>
<summary align="center"><b>🧪 Testing Without A Screen 🧪</b></summary>

<br>

<p align="center">
goome has a <b>test</b> backend that fakes a screen and plays a script of what the "user" does. Thats what all the tests here run on, no display needed:
</p>

```sh
zig build test --summary all
```

<p align="center">
You can test your own overlay the same way, either with env vars and no code changes:
</p>

```sh
GOOME_BACKEND=test GOOME_TEST_SCRIPT="1 click 400,300; 2 key hi\n; end 10" ./zig-out/bin/myapp
```

<p align="center">
or straight from Zig:
</p>

```zig
const g = try goome.Goome.open(.{ .backend = .@"test", .test_script = "screen 800x600 1; 1 click 120,90; end 5" });
```

<p align="center">
The script format is in the <a href="https://github.com/goome-ui/c-goome#readme">c-goome README</a>. The drawing, font, emoji, animation, IME, image and ui tests check the exact same pixel hashes as the tests in c-goome, on every OS, in Debug and ReleaseFast.
</p>
</details>

<details>
<summary align="center"><b>🔧 Updating goome 🔧</b></summary>

<br>

```sh
tools/update_native.sh ../c-goome      # or a path to any goome.h, or nothing to clone main
zig build test
```

<p align="center">
<code>native/VERSION</code> keeps the commit it came from and the package version follows goome.h. If the layout test fails after that, a struct changed and <code>src/goome.zig</code> needs a look.
</p>
</details>

<details>
<summary align="center"><b>🛠 Pull Requests 🛠</b></summary>

<br>

<p align="center">
Want to help with zig-goome? Make A pull request to <b>dev</b>!<br>
Small fixes are the easiest to merge, for anything bigger open an issue first so we can talk about it. Bugs in the C side go to <a href="https://github.com/goome-ui/c-goome">c-goome</a>.<br> <br>
As long as it works and doesn't add a dependency its very likely to get accepted!<br>
Read <a href="CONTRIBUTING.md">CONTRIBUTING.md</a> before you send one.
</p>
</details>

<details>
<summary align="center"><b>⚖️ License ⚖️</b></summary>

<br>

<p align="center">
zig-goome is under the <a href="LICENSE">GPL-3.0</a>.<br> <br>
<sub>
• You can use it, change it and share it<br>
• If you share something made with it, you have to share your source too, under the same license<br>
• Keep the credits
</sub><br> <br>
In short: play fair, keep it open, and give credit where it's due.
</p>
</details>

<details>
<summary align="center"><b>🩷 Donate 🩷</b></summary>

<br>

<p align="center">
<a href="https://sevvy-wevvy.com/kofi">Ko-fi</a> (Preferred)<br>
<a href="https://sevvy-wevvy.com/patreon">Patreon</a><br>
<a href="https://sevvy-wevvy.com/throne">Throne</a>
</p>
</details>
