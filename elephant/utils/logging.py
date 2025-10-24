"""Loguru 日志封装模块

基于 loguru 的统一日志系统，提供简单易用的日志接口。

特性：
- 统一的日志配置
- 支持控制台输出（默认）
- 支持文件输出（可选）
- 支持自定义日志级别和格式
- 线程安全

使用示例：
```python
from elephant.utils.logging import logger

logger.info("这是一条信息日志")
logger.debug("这是一条调试日志")
logger.warning("这是一条警告日志")
logger.error("这是一条错误日志")
logger.critical("这是一条严重错误日志")

# 带上下文的日志
logger.info("用户登录", user_id="alice", ip="192.168.1.1")

# 异常日志
try:
    1 / 0
except Exception as e:
    logger.exception("发生异常")
```
"""

import sys
from pathlib import Path
from typing import Optional, Union
from loguru import logger as _logger

# 默认日志格式
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 简洁格式（适合生产环境）
SIMPLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>"
)

# 详细格式（适合调试）
VERBOSE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<blue>{process}</blue>:<blue>{thread}</blue> - "
    "<level>{message}</level>"
)

# 全局日志器实例
logger = _logger

# 标记是否已初始化
_initialized = False


def setup_logger(
    level: str = "INFO",
    format_style: str = "default",
    custom_format: Optional[str] = None,
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    rotation: str = "10 MB",
    retention: str = "7 days",
    compression: str = "zip",
    enqueue: bool = True,
    colorize: bool = True,
    diagnose: bool = True,
) -> None:
    """配置全局日志器
    
    Args:
        level: 日志级别，可选值：TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
        format_style: 格式风格，可选值：default, simple, verbose
        custom_format: 自定义日志格式（如果提供，会覆盖 format_style）
        log_to_file: 是否同时输出到文件
        log_file_path: 日志文件路径（如果 log_to_file=True 但未指定，使用默认路径）
        rotation: 日志文件轮转策略（大小、时间等）
        retention: 日志文件保留策略
        compression: 日志文件压缩格式
        enqueue: 是否启用异步日志（多线程安全）
        colorize: 是否启用颜色输出
        diagnose: 是否启用详细诊断信息（异常堆栈）
    
    Examples:
        # 基本使用（默认配置）
        setup_logger()
        
        # 调试模式
        setup_logger(level="DEBUG", format_style="verbose")
        
        # 生产环境（输出到文件）
        setup_logger(
            level="INFO",
            format_style="simple",
            log_to_file=True,
            log_file_path="logs/app.log"
        )
        
        # 自定义格式
        setup_logger(
            custom_format="{time} | {level} | {message}",
            colorize=False
        )
    """
    global _initialized
    
    # 移除所有现有的处理器
    logger.remove()
    
    # 选择日志格式
    if custom_format:
        log_format = custom_format
    else:
        format_map = {
            "default": DEFAULT_FORMAT,
            "simple": SIMPLE_FORMAT,
            "verbose": VERBOSE_FORMAT,
        }
        log_format = format_map.get(format_style, DEFAULT_FORMAT)
    
    # 添加控制台输出
    logger.add(
        sys.stderr,
        format=log_format,
        level=level,
        colorize=colorize,
        enqueue=enqueue,
        diagnose=diagnose,
    )
    
    # 添加文件输出（如果需要）
    if log_to_file:
        if log_file_path is None:
            # 默认日志文件路径
            log_file_path = Path("logs") / "elephant_ai_{time:YYYY-MM-DD}.log"
        else:
            log_file_path = Path(log_file_path)
        
        # 确保日志目录存在
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            str(log_file_path),
            format=log_format,
            level=level,
            rotation=rotation,
            retention=retention,
            compression=compression,
            enqueue=enqueue,
            diagnose=diagnose,
        )
        
        logger.info(f"日志文件输出已启用: {log_file_path}")
    
    _initialized = True
    logger.success(f"日志系统初始化完成 (级别: {level}, 格式: {format_style or 'custom'})")


def get_logger(name: Optional[str] = None):
    """获取日志器实例
    
    Args:
        name: 日志器名称（通常传入 __name__），用于日志上下文
    
    Returns:
        配置好的 loguru logger 实例
    
    Note:
        这个函数主要是为了兼容性，实际上 loguru 的 logger 是全局单例。
        name 参数会被添加到日志的上下文中，但不会创建独立的 logger。
    """
    # 如果还没初始化，使用默认配置初始化
    if not _initialized:
        setup_logger()
    
    # loguru 的 logger 是全局单例，但可以通过 bind 添加上下文
    if name:
        return logger.bind(module=name)
    return logger


# 默认初始化（使用默认配置）
if not _initialized:
    setup_logger()


# 导出常用方法（方便直接调用）
trace = logger.trace
debug = logger.debug
info = logger.info
success = logger.success
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception


__all__ = [
    "logger",
    "setup_logger",
    "get_logger",
    "trace",
    "debug",
    "info",
    "success",
    "warning",
    "error",
    "critical",
    "exception",
    "DEFAULT_FORMAT",
    "SIMPLE_FORMAT",
    "VERBOSE_FORMAT",
]
