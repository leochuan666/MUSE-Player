# 🧹 MUSE Player 仓库清理清单

> ⚠️ 所有删除操作需你逐项确认后再执行。不删除任何业务代码。

---

## ✅ 必须保留 (Keep)

| 文件 | 用途 |
|------|------|
| `index.html` | 主应用，2433行 |
| `manifest.json` | PWA manifest |
| `favicon.svg` | 网站图标 |
| `icons/icon-192x192.png` | PWA 192px图标 |
| `icons/icon-512x512.png` | PWA 512px图标 |
| `icons/icon.svg` | PWA SVG图标 |
| `icons/MUSE.ico` | Windows图标 |
| `icons/muse-screenshot.png` | 演示截图（比赛用） |
| `icons/muse-ai-icon.png` | AI图标素材 |
| `launch-muse.bat` | 一键启动脚本 |
| `package.json` | npm依赖声明 |
| `docs/superpowers/specs/2026-05-21-muse-player-design.md` | 设计文档（将移至 docs/DESIGN.md） |

### lx-api-server/ 保留（核心运行所需）

| 文件/目录 | 用途 |
|-----------|------|
| `main.py` | 入口 |
| `api/` | API处理模块 |
| `crypt/` | 加解密模块 |
| `data/config.json` | 配置文件 |
| `middleware/` | 认证+日志中间件 |
| `modules/` | 核心模块（info/lyric/plat/refresh/url） |
| `server/` | 服务器配置 |
| `utils/` | 工具函数集 |
| `requirements.txt` | Python依赖 |
| `pyproject.toml` | Python项目配置 |
| `package.json` | Node依赖 |
| `clean.py` | 清理脚本 |
| `.gitignore` | Git忽略规则 |

---

## 🔴 必须删除 (Delete)

### 根目录杂物
| 文件 | 原因 |
|------|------|
| `index_clean_closing.txt` | 历史备份 |
| `index_clean_html_css.txt` | 历史备份 |
| `launcher.html` | 与 launch-muse.bat 功能重复 |
| `preview-ui.html` | 预览原型 |
| `preview-v3.html` | 预览原型 |
| `preview-variants.html` | 预览原型 |
| `preview-aura-fusion.html` | 预览原型 |
| `package-lock.json` | npm install 生成 |
| `node_modules/` | 不应提交 |
| `.superpowers/` | 内部工具目录 |
| `aura_ref/pic_1.png` | 参考素材 |
| `aura_ref/pic_2.png` | 参考素材 |
| `aura_ref/` (空目录) | — |
| `icons/muse-v1.png` | 低质量版本 |
| `icons/muse-v2.png` | 低质量版本 |
| `icons/muse-v3.png` | 低质量版本 |

### lx-api-server/ 删除
| 文件/目录 | 原因 |
|-----------|------|
| `.github/` | 上游CI配置 |
| `.vscode/` | 上游IDE配置 |
| `.pre-commit-config.yaml` | 上游开发工具 |
| `.python-version` | 上游开发配置 |
| `uv.lock` | uv包管理器锁文件 |
| `README.md` | 上游README |
| `README_EN.md` | 上游README |
| `LICENSE` | 上游许可证 |
| `docs/` | 上游文档站 |
| `mkdocs.yml` | 上游文档配置 |
| `res/` | 上游资源文件 |
| `static/lx-source.js` | 上游前端脚本（MUSE未使用） |
| `data/cache/device.json` | 缓存文件 |

---

## 🟡 建议归档 (Archive to archive/)

如果你不想彻底删除以下文件，可移到 `archive/` 目录：

| 文件 | 原因 |
|------|------|
| `preview-ui.html` | 初版预览，可能有参考价值 |
| `preview-v3.html` | 第三版预览 |
| `preview-variants.html` | 变体预览 |
| `preview-aura-fusion.html` | 极光融合实验 |
| `launcher.html` | 旧版启动器 |
| `icons/muse-v1.png` ~ `muse-v3.png` | 旧版图标 |
| `aura_ref/pic_1.png` ~ `pic_2.png` | 参考图 |
| `index_clean_closing.txt` | 代码片段备份 |
| `index_clean_html_css.txt` | 代码片段备份 |

---

## 📊 统计

| 类别 | 数量 |
|------|------|
| 必须保留 | ~80 文件 |
| 必须删除 | ~28 文件 |
| 建议归档 | ~11 文件 |
| 删除后 lx-api-server/ | 仅剩运行必需的 ~55 文件 |

---

## ⚡ 执行确认

请回复以下之一：
- **"全部执行"** — 按上表删除所有 🔴 + 归档所有 🟡
- **"只删除不归档"** — 🔴 全部删除，🟡 也直接删除
- **"逐项确认"** — 我一步步问你
- **"xx 保留"** — 指定不想删的文件
