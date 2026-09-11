"""独立演示：等待 3 秒，采集 5 秒，停止后保存最后结果。"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from time import sleep

import numpy as np

# 支持直接执行带版本号目录内的脚本；不实现主程序插件发现机制。
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from capture import GDIWorker  # noqa: E402

from phantom.captures.contracts import CaptureResult  # noqa: E402


def save_result(result: CaptureResult) -> Path:
    output = (
        Path(__file__).resolve().parent
        / "demo_results"
        / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    )
    output.mkdir(parents=True, exist_ok=False)
    if result.image is not None:
        np.save(output / "result.npy", result.image, allow_pickle=False)
    (output / "result.txt").write_text(
        json.dumps(asdict(result.status), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return output


def main() -> None:
    worker = GDIWorker(fps=15)
    print("3 秒后开始截图，运行 5 秒后停止。", flush=True)
    try:
        sleep(3)
        worker.start()
        sleep(5)
    finally:
        worker.stop()
    output = save_result(worker.get_latest_result())
    print(f"最后结果已保存：{output}")


if __name__ == "__main__":
    main()
