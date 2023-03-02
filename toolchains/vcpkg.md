## 快速开始: Windows

linux运行sh就可以了。

```cmd
> git clone https://github.com/microsoft/vcpkg
> .\vcpkg\bootstrap-vcpkg.bat
```

使用以下命令安装您的项目所需要的库：

```cmd
> .\vcpkg\vcpkg install [packages to install]
```

请注意: vcpkg 在 Windows 中默认编译并安装 x86 版本的库。 若要编译并安装 x64 版本，请执行:

```cmd
> .\vcpkg\vcpkg install [package name]:x64-windows
```

或

```cmd
> .\vcpkg\vcpkg install [packages to install] --triplet=x64-windows
```

您也可以使用 `search` 子命令来查找 vcpkg 中集成的库:

```cmd
> .\vcpkg\vcpkg search [search term]
```

若您希望在 Visual Studio 中使用 vcpkg，请运行以下命令 (可能需要管理员权限)

```cmd
> .\vcpkg\vcpkg integrate install
```

在此之后，您可以创建一个非 CMake 项目 (或打开已有的项目)。
在您的项目中，所有已安装的库均可立即使用 `#include` 包含您需使用的库的头文件且无需额外配置。

若您在 Visual Studio 中使用 CMake 工程，请查阅[这里](#visual-studio-cmake-工程中使用-vcpkg)。

为了在 IDE 以外在 CMake 中使用 vcpkg，您需要使用以下工具链文件:

```cmd
> cmake -B [build directory] -S . "-DCMAKE_TOOLCHAIN_FILE=[path to vcpkg]/scripts/buildsystems/vcpkg.cmake"
> cmake --build [build directory]
```

在 CMake 中，您仍需通过 `find_package` 来使用 vcpkg 中已安装的库。
请查阅 [CMake 章节](#在-cmake-中使用-vcpkg) 获取更多信息，其中包含了在 IDE 中使用 CMake 的内容。

对于其他工具 (包括 Visual Studio Code)，请查阅 [集成指南][getting-started:integration]。

## 在 CMake 中使用 vcpkg

### Visual Studio CMake 工程中使用 vcpkg

打开 CMake 设置选项，将 vcpkg toolchain 文件路径在 `CMake toolchain file` 中：

```
[vcpkg root]/scripts/buildsystems/vcpkg.cmake
```

### CLion 中使用 vcpkg

打开 Toolchains 设置
(File > Settings on Windows and Linux, CLion > Preferences on macOS)，
并打开 CMake 设置 (Build, Execution, Deployment > CMake)。
最后在 `CMake options` 中添加以下行:

```
-DCMAKE_TOOLCHAIN_FILE=[vcpkg root]/scripts/buildsystems/vcpkg.cmake
```

您必须手动将此选项加入每个项目配置文件中。