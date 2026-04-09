# project-documentation

项目文档 - 自动化部署

## 文件说明
## 📁 项目文件列表

- `MEMORY.md`
- `IDENTITY.md`
- `USER.md`
- `SOUL.md`
- `AGENTS.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `memory/2026-03-27.md`
- `memory/2026-03-28.md`
- `memory/2026-03-29.md`
- `memory/2026-03-30.md`
- `memory/2026-03-31.md`
- `memory/2026-04-01.md`
- `memory/2026-04-02.md`
- `memory/2026-04-03.md`
- `memory/2026-04-04.md`
- `memory/2026-04-06.md`
- `memory/2026-04-09.md`
- `final_completion_report.md`
- `quality_improvement_report.md`
- `final_13_ai_skills_completion_report.md`
- `13_ai_skills_report.md`
- `skill_analysis_report.md`
- `project_discovery_report.md`
- `top_10_projects_report.md`
- `youtube-opportunities-report.md`
- `全自动化赚钱项目-2026.md`
- `完整项目执行系统.md`
- `科技赚钱快速指南.md`
- `财富创造管道总览.md`
- `赚钱研究Agent配置.md`
- `赚钱项目数据库.md`
- `claude_code_hotspot_strategy.md`
- `claude_code_12_skills_package.md`
- `autonomous_search_skill_plan.md`
- `project_function_enhancement_plan.md`
- `lobster_director_project_plan.md`
- `全力自主执行计划.md`
- `全自动盈利项目工厂系统.md`
- `全项目并行执行计划.md`
- `发布完成确认.md`
- `夜间任务更新.md`
- `安全清理确认.md`
- `立即行动清单.md`
- `系统健康报告调整总结.md`
- `自主修复脚本.py`
- `自主执行计划.md`
- `高速项目执行系统.md`
- `今日头条文章分析.md`
- `toutiao_video_ai_analysis.md`
- `infinite_memory_system/技术深度优化/语义引擎测试报告.md`
- `infinite_memory_system/技术深度优化/第1周-算法升级/语义关联算法/semantic_engine.py`

这是一个自动化生成的GitHub仓库。

## 部署状态
- ✅ 仓库创建完成
- ⚡ 文件准备中
- 🚀 即将推送完整项目

## 联系
- GitHub: [fabio2026-ui](https://github.com/fabio2026-ui)
- Email: fufansong@gmail.com

## 🐳 Docker 部署
## 🧪 测试

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 运行特定测试文件
pytest tests/test_project_documentation.py

# 运行集成测试
pytest tests/test_integration_project_documentation.py -v
```

### 测试覆盖率

项目使用pytest-cov进行测试覆盖率统计。目标覆盖率:

- **单元测试**: ≥80%
- **集成测试**: ≥70%
- **总体覆盖率**: ≥75%

### 测试类型

1. **单元测试**: 测试单个函数和类
2. **集成测试**: 测试组件之间的交互
3. **端到端测试**: 测试完整工作流程
4. **性能测试**: 测试系统性能
5. **安全测试**: 测试安全漏洞

### 持续集成

GitHub Actions自动运行测试:
- 每次推送到main分支
- 每次拉取请求
- 每天凌晨自动运行

### 测试报告

测试报告可在以下位置查看:
- **GitHub Actions**: 工作流运行详情
- **Codecov**: 代码覆盖率报告
- **测试产物**: HTML覆盖率报告

### 测试最佳实践

- 每个测试应该独立运行
- 使用fixture进行测试数据准备
- 模拟外部依赖
- 测试边界情况和错误场景
- 保持测试快速运行

## 📦 GitHub Container Registry

### 自动构建的容器镜像

每次推送到main分支时，GitHub Actions会自动构建并推送Docker镜像到GitHub Container Registry。

**镜像地址**: `ghcr.io/fabio2026-ui/project-documentation:latest`

### 拉取和使用镜像

```bash
# 拉取最新镜像
docker pull ghcr.io/fabio2026-ui/project-documentation:latest

# 运行容器
docker run -d -p 8080:8000 --name project-documentation ghcr.io/fabio2026-ui/project-documentation:latest

# 使用docker-compose
version: '3.8'
services:
  project-documentation:
    image: ghcr.io/fabio2026-ui/project-documentation:latest
    ports:
      - "8080:8000"
```

### 手动构建和推送

```bash
# 登录到GitHub Container Registry
echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin

# 构建镜像
docker build -t ghcr.io/fabio2026-ui/project-documentation:latest .

# 推送镜像
docker push ghcr.io/fabio2026-ui/project-documentation:latest
```


### 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/fabio2026-ui/project-documentation.git
   cd project-documentation
   ```

2. **使用Docker部署**
   ```bash
   # 方法1: 使用部署脚本
   ./deploy.sh
   
   # 方法2: 手动部署
   docker-compose build
   docker-compose up -d
   ```

3. **访问应用**
   - 本地访问: http://localhost:8080
   - 容器状态: `docker ps | grep project-documentation`
   - 查看日志: `docker logs project-documentation`

### 管理命令

```bash
# 停止容器
docker-compose down

# 重启容器
docker-compose restart

# 查看日志
docker-compose logs -f

# 进入容器
docker exec -it project-documentation bash
```

### 生产环境部署

对于生产环境，建议使用:
- **Docker Swarm** 或 **Kubernetes** 进行容器编排
- **Traefik** 或 **Nginx** 作为反向代理
- **Let's Encrypt** 进行SSL证书管理
