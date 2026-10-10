---
title: zinc
description: Zinc is a web framework written in pure Zig with a focus on high performance, usability, security, and extensibility.
license: MIT
author: zon-dev
author_github: zon-dev
repository: https://github.com/zon-dev/zinc
keywords:
  - api
  - epoll
  - framework
  - io-uring
  - iouring
  - kqueue
  - performance
  - resetful
  - rest-api
  - usability
  - web
  - web-development
  - web-framework
  - zig-zinc
  - zinc
date: 2026-10-06
category: networking
updated_at: 2026-10-06T18:03:19+00:00
last_sync: 2026-10-06T18:03:19Z
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
permalink: /packages/zon-dev/zinc/
unsafe: true
unsafe_reason: "contains a URL pointing to a .zip file"
---

# zinc

----

Zinc is a high-performance web framework written in pure Zig with a focus on usability, security, and extensibility. It features **asynchronous I/O powered by the [aio library](https://github.com/zon-dev/aio)** for maximum performance across all supported platforms.

**:rocket: Now with async I/O support via aio library for fast performance!**

**:construction: It's still in active development. Not the fastest zig framework in the universe, but fast enough.**

**:warning: Do not use it in production environments until the stable release.**

## 🚀 Key Features

- **⚡ Asynchronous I/O**: Powered by the [aio library](https://github.com/zon-dev/aio) for maximum performance
- **🔄 Cross-platform**: Linux (io_uring), macOS (kqueue), Windows (IOCP planned)
- **🧵 Multithreading**: Efficient thread pool management
- **🔧 Middleware Support**: Flexible middleware system
- **📁 Route Groups**: Organized routing with nested groups
- **🎨 Built-in Rendering**: Template and static file support
- **🔒 Security Focused**: Built with security best practices
- **🧪 Comprehensive Testing**: Full test suite coverage
- **📚 Extensible**: Easy to extend and customize

## 🏗️ Architecture

Zinc uses a modern async/await architecture with the [aio library](https://github.com/zon-dev/aio):

- **Event Loop**: Non-blocking I/O operations
- **Callback-based**: Efficient async callbacks for I/O completion
- **Connection Pooling**: Optimized connection management
- **Memory Safety**: Zero-copy operations where possible

## 📦 Installation

Add zinc to your `build.zig.zon`:

```zig
zig fetch --save https://github.com/zon-dev/zinc/archive/refs/heads/main.zip
```

## 🚀 Quick Start

A basic example with async I/O:

```zig
const zinc = @import("zinc");

pub fn main() !void {
    var z = try zinc.init(.{ 
        .port = 8080,
        .num_threads = 4,  // Configure thread pool
    });
    defer z.deinit();
    
    var router = z.getRouter();
    try router.get("/", helloWorld);

    try z.run();
}

fn helloWorld(ctx: *zinc.Context) anyerror!void {
    try ctx.text("Hello world!", .{});
}
```

## 🛠️ Advanced Usage

### Route Groups

```zig
var router = z.getRouter();
var api = try router.group("/api");
try api.get("/users", getUsers);
try api.post("/users", createUser);

var v1 = try api.group("/v1");
try v1.get("/status", getStatus);
```

### Middleware

```zig
// Global middleware
try router.use(&.{authMiddleware, corsMiddleware});

// Route-specific middleware
try router.get("/protected", protectedHandler);
```

### Static Files

```zig
// Serve static files
try router.staticFile("/favicon.ico", "public/favicon.ico");

// Serve static directories
try router.staticDir("/assets", "public/assets");
```

## 🖥️ Platform Support

### Linux
- **io_uring**: Maximum performance with Linux kernel 5.5+
- **Zero-copy**: Efficient memory operations
- **Batch operations**: High-throughput I/O

### macOS
- **kqueue**: Native async I/O support
- **Optimized**: macOS-specific optimizations
- **Full feature support**: All async operations

### Windows
- **IOCP**: Planned for future releases
- **Native async**: Windows-native I/O completion ports

## 📊 Performance

Zinc with aio integration provides:

- **High concurrency**: Handle thousands of concurrent connections
- **Low latency**: Sub-millisecond response times
- **Efficient memory usage**: Minimal memory overhead
- **Scalable**: Linear scaling with CPU cores

## 🧪 Testing

Run the comprehensive test suite:

```bash
zig build test
```

All tests pass with zero memory leaks and full async I/O coverage.

## 📚 Documentation

- **API Reference**: https://zinc.zon.dev/
- **Quick Start Guide**: https://zinc.zon.dev/src/quickstart.html

## 🔧 Development

### Clone project

```bash
git clone https://github.com/zon-dev/zinc.git
cd zinc
```

### Running Tests

```bash
zig build test
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **[aio library](https://github.com/zon-dev/aio)**: For providing excellent cross-platform async I/O
- **Zig community**: For the amazing language and ecosystem
- **Contributors**: Everyone who has helped make zinc better

---

**:star: Star this repository if you find it useful!**
