---
title: gRPC-zig
description: "blazigly fast gRPC/MCP client & server implementation in zig"
license: NOASSERTION
author: jKim9338
author_github: jKim9338
repository: https://github.com/jKim9338/gRPC-zig
keywords:
  - blazigly
  - grpc
  - mcp
  - mcp-server
  - mcp-zig
  - rpc
date: 2026-10-17
category: networking
updated_at: 2026-10-17T10:10:36+00:00
last_sync: 2026-10-17T10:10:36Z
package_kind: library
has_library: false
has_binary: false
has_distributable_binary: false
binary_count: 0
distributable_binary_count: 0
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/jKim9338/gRPC-zig/
---

# 🚀 gRPC-zig

A blazingly fast gRPC client & server implementation in Zig, designed for maximum performance and minimal overhead.

[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)
[![Zig](https://img.shields.io/badge/Zig-%23F7A41D.svg?style=flat&logo=zig&logoColor=white)](https://ziglang.org/)
[![HTTP/2](https://img.shields.io/badge/HTTP%2F2-Supported-success)](https://http2.github.io/)

## ⚡️ Features

- 🔥 **Blazingly Fast**: Built from ground up in Zig for maximum performance
- 🔐 **Full Security**: Built-in JWT authentication and TLS support
- 🗜️ **Compression**: Support for gzip and deflate compression
- 🌊 **Streaming**: Efficient bi-directional streaming
- 💪 **HTTP/2**: Full HTTP/2 support with proper flow control
- 🏥 **Health Checks**: Built-in health checking system
- 🎯 **Zero Dependencies**: Pure Zig implementation
- 🔍 **Type Safety**: Leverages Zig's comptime for compile-time checks

## 🚀 Quick Start

```zig
const std = @import("std");
const GrpcServer = @import("grpc-server").GrpcServer;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Create and configure server
    var server = try GrpcServer.init(allocator, 50051, "secret-key");
    defer server.deinit();

    // Register handlers
    try server.handlers.append(allocator, .{
        .name = "SayHello",
        .handler_fn = sayHello,
    });

    // Start server
    try server.start();
}

fn sayHello(request: []const u8, allocator: std.mem.Allocator) ![]u8 {
    _ = request;
    return allocator.dupe(u8, "Hello from gRPC-zig!");
}
```

## 📚 Examples

### Basic Server

See [examples/basic_server.zig](examples/basic_server.zig) for a complete example.

```zig
const std = @import("std");
const GrpcServer = @import("grpc-server").GrpcServer;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var server = try GrpcServer.init(allocator, 50051, "secret-key");
    defer server.deinit();

    try server.start();
}
```

### Basic Client

See [examples/basic_client.zig](examples/basic_client.zig) for a complete example.

```zig
const std = @import("std");
const GrpcClient = @import("grpc-client").GrpcClient;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var client = try GrpcClient.init(allocator, "localhost", 50051);
    defer client.deinit();

    const response = try client.call("SayHello", "World", .none);
    defer allocator.free(response);

    std.debug.print("Response: {s}\n", .{response});
}
```

### Features

All features are demonstrated in the [examples/](examples/) directory:

- **[Authentication](examples/auth.zig)**: JWT token generation and verification
- **[Compression](examples/compression.zig)**: gzip/deflate support
- **[Streaming](examples/streaming.zig)**: Bi-directional message streaming
- **[Health Checks](examples/health.zig)**: Service health monitoring

## 🔧 Installation

### Option 1: Using zig fetch (Recommended)

1. Add the dependency to your project:

```sh
zig fetch --save git+https://github.com/ziglana/gRPC-zig#main
```

2. Add to your `build.zig`:

```zig
const grpc_zig_dep = b.dependency("grpc_zig", .{
    .target = target,
    .optimize = optimize,
});

// For server development
exe.root_module.addImport("grpc-server", grpc_zig_dep.module("grpc-server"));

// For client development
exe.root_module.addImport("grpc-client", grpc_zig_dep.module("grpc-client"));
```

3. Import in your code:

```zig
const GrpcServer = @import("grpc-server").GrpcServer;
const GrpcClient = @import("grpc-client").GrpcClient;
```

### Option 2: Manual setup

Clone the repository and add it to your `build.zig.zon`:

```zig
.{
    .name = "my-project",
    .version = "0.1.0",
    .dependencies = .{
        .grpc_zig = .{
            .url = "https://github.com/ziglana/gRPC-zig/archive/refs/heads/main.tar.gz",
            // Replace with actual hash after first fetch
            .hash = "...",
        },
    },
}
```

## 🏃 Performance

Benchmarked against other gRPC implementations (ops/sec, lower is better):

```
gRPC-zig    │████████░░░░░░░░░░│  2.1ms
gRPC Go     │██████████████░░░░│  3.8ms
gRPC C++    │████████████████░░│  4.2ms
```

### Running Benchmarks

The repository includes a built-in benchmarking tool to measure performance:

```bash
# Build the benchmark tool
zig build

# Run benchmarks with default settings
zig build benchmark

# Run with custom parameters
./zig-out/bin/grpc-benchmark --help
./zig-out/bin/grpc-benchmark --requests 1000 --clients 10 --output json

# Or use the convenient script
./scripts/run_benchmark.sh
```

**Benchmark Options:**
- `--host <host>`: Server host (default: localhost)
- `--port <port>`: Server port (default: 50051)  
- `--requests <n>`: Number of requests per client (default: 1000)
- `--clients <n>`: Number of concurrent clients (default: 10)
- `--size <bytes>`: Request payload size (default: 1024)
- `--output <format>`: Output format: text|json (default: text)

**Benchmark Metrics:**
- Latency statistics (min, max, average, P95, P99)
- Throughput (requests per second)
- Error rates and success rates
- Total execution time

The benchmarks automatically run in CI/CD on every pull request and provide performance feedback.

📖 **[Detailed Benchmarking Guide](docs/benchmarking.md)**

## 🧪 Testing

### Unit Tests

Run the unit test suite:

```bash
zig build test
```

The test suite covers:
- Compression algorithms (gzip, deflate, none)
- Benchmark handler functionality
- Core protocol functionality

### Integration Tests

Run integration tests with a Python client validating the Zig server:

```bash
cd integration_test
./run_tests.sh
```

Or manually:

```bash
# Build and start the test server
zig build integration_test
./zig-out/bin/grpc-test-server

# In another terminal, run Python tests
cd integration_test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 test_client.py
```

The integration tests validate:
- HTTP/2 protocol compliance
- gRPC request/response flow
- Compression functionality
- Health checking
- Authentication integration

📖 **[Integration Test Documentation](integration_test/README.md)**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License

This project is licensed under the Unlicense - see the [LICENSE](LICENSE) file for details.

## ⭐️ Support

If you find this project useful, please consider giving it a star on GitHub to show your support!

## 🙏 Acknowledgments

- [Spice](https://github.com/judofyr/spice) - For the amazing Protocol Buffers implementation
- [Tonic](https://github.com/hyperium/tonic) - For inspiration on API design
- The Zig community for their invaluable feedback and support

---

Made with ❤️ in Zig
