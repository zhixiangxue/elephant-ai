"""HelloAgents记忆系统模块

按照命名规范的分层记忆系统：

核心类：
- Memory: 记忆系统统一接口（核心管理类）
- Memo: 记忆备忘录（数据传输对象）
- Config: 记忆系统配置
- BaseMemory: 记忆类型基类

使用示例：
```python
from memory import Memory, Memo, Config

config = Config(storage_path="./data")
mem = Memory(config=config, user_id="alice")

# 添加记忆
memo_id = mem.add("今天学习了AI Agent")

# 检索记忆
memos = mem.retrieve("AI Agent")
```
"""

# Core Layer (记忆核心层)
from .core import Memory

# Memory Types Layer (记忆类型层)
from .types.working import WorkingMemory
from .types.episodic import EpisodicMemory
from .types.semantic import SemanticMemory
from .types.perceptual import PerceptualMemory

# Storage Layer (存储层)
from .storage.document_store import DocumentStore, SQLiteDocumentStore

# Base classes and utilities
from .base import Memo, Config, BaseMemory

__all__ = [
    # Core
    "Memory",

    # Memory Types
    "WorkingMemory",
    "EpisodicMemory",
    "SemanticMemory",
    "PerceptualMemory",

    # Storage Layer
    "DocumentStore",
    "SQLiteDocumentStore",

    # Base
    "Memo",
    "Config",
    "BaseMemory",
]
