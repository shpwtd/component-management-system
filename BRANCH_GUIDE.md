# Git 分支管理指南

## 当前分支结构

```
main (稳定版本)
  └── v1.0.0 (标签)
```

## 分支说明

### 🌿 main (主分支)
- **用途**: 生产环境稳定版本
- **保护**: 只接受来自 develop 或 hotfix 的合并
- **更新频率**: 低(发布新版本时)

### 🔧 develop (开发分支) - 建议创建
```bash
git checkout -b develop
```
- **用途**: 日常开发集成分支
- **来源**: 从 main 分支创建
- **合并目标**: 测试完成后合并回 main

### ✨ feature/* (功能分支)
```bash
git checkout -b feature/数据库迁移
git checkout -b feature/CSRF保护
```
- **用途**: 新功能开发
- **命名规范**: `feature/功能名称`
- **生命周期**: 功能完成后合并到 develop,然后删除

### 🐛 hotfix/* (紧急修复分支)
```bash
git checkout -b hotfix/修复库存计算错误
```
- **用途**: 生产环境紧急bug修复
- **来源**: 从 main 分支创建
- **合并目标**: 同时合并到 main 和 develop

## 工作流程示例

### 开发新功能

```bash
# 1. 切换到 develop 分支
git checkout develop

# 2. 创建功能分支
git checkout -b feature/智能搜索优化

# 3. 开发并提交
git add .
git commit -m "feat: 实现多条件组合搜索"

# 4. 推送到远程(如有)
git push origin feature/智能搜索优化

# 5. 完成后合并到 develop
git checkout develop
git merge feature/智能搜索优化
git branch -d feature/智能搜索优化
```

### 发布新版本

```bash
# 1. 从 develop 创建 release 分支
git checkout -b release/v1.1.0 develop

# 2. 进行最后的测试和文档更新
git commit -m "docs: 更新v1.1.0发布说明"

# 3. 合并到 main 并打标签
git checkout main
git merge release/v1.1.0
git tag -a v1.1.0 -m "Release v1.1.0"

# 4. 合并回 develop
git checkout develop
git merge release/v1.1.0

# 5. 删除 release 分支
git branch -d release/v1.1.0
```

### 紧急修复

```bash
# 1. 从 main 创建 hotfix 分支
git checkout main
git checkout -b hotfix/修复数据丢失bug

# 2. 修复并提交
git add .
git commit -m "fix: 修复并发写入导致的数据丢失问题"

# 3. 合并到 main 并打标签
git checkout main
git merge hotfix/修复数据丢失bug
git tag -a v1.0.1 -m "Hotfix v1.0.1"

# 4. 合并到 develop
git checkout develop
git merge hotfix/修复数据丢失bug

# 5. 删除 hotfix 分支
git branch -d hotfix/修复数据丢失bug
```

## 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Type 类型

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档变更
- `style`: 代码格式(不影响功能)
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

### 示例

```bash
git commit -m "feat(search): 添加多条件组合搜索功能"
git commit -m "fix(stock): 修复出库数量验证逻辑"
git commit -m "docs(readme): 更新安装说明"
git commit -m "refactor(classifier): 重构分类算法提高可维护性"
git commit -m "perf(ui): 优化首页加载速度"
```

## 常用命令速查

```bash
# 查看分支
git branch
git branch -a          # 查看所有分支(包括远程)

# 切换分支
git checkout <branch-name>
git switch <branch-name>  # Git 2.23+

# 创建并切换分支
git checkout -b <branch-name>

# 合并分支
git merge <branch-name>

# 删除分支
git branch -d <branch-name>     # 本地
git push origin --delete <branch-name>  # 远程

# 查看历史
git log --oneline --graph -10
git log --pretty=format:"%h - %an, %ar : %s"

# 查看标签
git tag
git tag -l "v1.*"

# 暂存更改
git stash
git stash pop

# 撤销操作
git reset --soft HEAD~1    # 撤销最后一次提交,保留更改
git reset --hard HEAD~1    # 撤销最后一次提交,丢弃更改(危险!)
git revert <commit-hash>   # 创建新的提交来撤销某次提交(安全)
```

## 注意事项

⚠️ **重要提醒**:

1. **不要在 main 分支直接开发**
2. **合并前确保代码通过测试**
3. **保持提交原子性**(一个提交只做一件事)
4. **及时清理已合并的分支**
5. **定期同步远程仓库** `git fetch --all`
6. **敏感数据不要提交** (已在 .gitignore 中配置)

## 下一步建议

1. 创建远程仓库(GitHub/Gitee/GitLab)
2. 设置分支保护规则
3. 配置 CI/CD 自动化测试
4. 添加 Code Review 流程

---

最后更新: 2026-07-01
