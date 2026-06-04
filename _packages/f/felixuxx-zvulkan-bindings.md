---
title: zvulkan-bindings
description: Zero-dependency, modular Vulkan bindings for Zig
license: MIT
author: felixuxx
author_github: felixuxx
repository: https://github.com/felixuxx/zvulkan-bindings
keywords:
  - gamedev
  - vulkan
  - vulkan-api
date: 2026-06-04
category: game-development
updated_at: 2026-06-04T13:21:16+00:00
last_sync: 2026-06-04T13:21:16Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/felixuxx/zvulkan-bindings/
---

# zvulkan-bindings

Comprehensive, zero-c-dependency, modular Vulkan bindings for Zig 0.15.2.

## Goals

The primary goal of this project is to provide a clean, idiomatic,
and robust interface to the Vulkan API for Zig game engines and applications,
without relying on C header translation (`@cImport`) or external generator
scripts during the build process.

### Key Features

* **Zero Dependencies**: Pure Zig implementation. No generic `vulkan.h`
translation.
* **Modular Architecture**: Core API versions (1.0, 1.1, 1.2, 1.3) are separated
into distinct modules, allowing you to use strictly what you need.
* **Dynamic Loading**: Built-in support for loading the Vulkan runtime
(`libvulkan.so`, `vulkan-1.dll`, etc.) dynamically at runtime. This allows your
application to start even if Vulkan is not present, or to handle partial
support gracefully.
* **WSI Support**: Built-in support for Window System Integration extensions
(`VK_KHR_surface`, `VK_KHR_swapchain`) and platform-specific surfaces
(Wayland, XCB, Xlib, Win32).
* **Type Safety**: Proper Zig enums, packed structs for flags,
and optional pointers to ensure type safety where possible while maintaining the
raw API mapping.

## Status

| Module | Status | Description |
| :--- | :--- | :--- |
| **Loader** | ✅ Ready | Dynamic loading and dispatch table generation. |
| **Core 1.0** | ✅ Ready | Base API commands, memory, resources. |
| **Core 1.1** | ✅ Ready | `PhysicalDeviceFeatures2`, Device Groups, Subgroups. |
| **Core 1.2** | ✅ Ready | Timeline Semaphores, Buffer Device Address. |
| **Core 1.3** | ✅ Ready | Dynamic Rendering, Synchronization2, Private Data. |
| **WSI** | ✅ Ready | Surfaces, Swapchains, Platform Integrations. |

## Installation

Add this package to your `build.zig.zon`:

```bash
zig fetch --save git+https://github.com/felixuxx/zvulkan-bindings.git
```

## Usage

In your `build.zig`:

```zig
const zvulkan = b.dependency("zvulkan_bindings", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("zvulkan_bindings", zvulkan.module("zvulkan_bindings"));
```

In your code:

```zig
const std = @import("std");
const vk = @import("zvulkan_bindings");

pub fn main() !void {
    // 1. Initialize Loader (dynamically loads libvulkan)
    var loader = try vk.Loader.init();
    defer loader.deinit();

    // 2. Create Instance
    var instance: vk.Instance = undefined;
    const app_info = vk.core_1_0.ApplicationInfo{
        .api_version = vk.constants.makeApiVersion(0, 1, 3, 0), // Request Vulkan 1.3
        ...
    };
    _ = loader.vkCreateInstance.?(&create_info, null, &instance);

    // 3. Load Instance Functions
    const instance_dispatch = try loader.createInstanceDispatch(instance);
    
    // 4. Use Global/Instance Functions
    // (Core 1.0 functions act as standard, 1.1+ may be optional depending on driver support)
    var device_count: u32 = 0;
    _ = instance_dispatch.vkEnumeratePhysicalDevices(instance, &device_count, null);
}
```
