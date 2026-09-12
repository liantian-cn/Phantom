"""
Summary:
    从启动工作目录加载配置并运行 Phantom Textual 主程序。
Description:
    配置错误在进入终端界面前明确报告；正常退出或异常离开都释放后台资源。
Key Variables:
    working_directory: 系统传给程序的启动工作目录，与源码位置无关。
Change Log:
    2026-09-11: Added Python 工程基础入口。
    2026-09-12: Changed 接入工作目录配置与 Textual 采集界面。
"""

import sys
from pathlib import Path

from phantom.core.configuration import ConfigurationError, load_config
from phantom.ui.app import PhantomApp


def main() -> None:
    working_directory = Path.cwd()
    try:
        config = load_config(working_directory)
    except ConfigurationError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
    app = PhantomApp(config)
    try:
        app.run()
    finally:
        app.close_resources()


if __name__ == "__main__":
    main()
