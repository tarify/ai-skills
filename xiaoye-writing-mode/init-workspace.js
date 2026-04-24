#!/usr/bin/env node
/**
 * Writing Mode 自动初始化函数
 * 在 skill 执行时自动检查和创建缺失的配置文件
 *
 * 使用方式：
 *   const initWorkspace = require('./init-workspace.js');
 *   await initWorkspace(workspacePath);
 *
 * 直接执行：
 *   node init-workspace.js [工作区路径]
 *   node init-workspace.js /path/to/your/novel/project
 */

const fs = require('fs').promises;
const path = require('path');

// Scaffold 源目录（位于 skill 目录下）
const SCAFFOLD_DIR = path.join(__dirname, 'scaffold');

// 必需加载的文件列表（基于 SKILL.md 规范）
const REQUIRED_FILES = [
  'AGENTS.md',
  'SOUL.md',
  'MEMORY.md',
  'rules/写作规范.md',
  'rules/评审标准.md',
  'rules/管理流程.md',
  'templates/辩证分析模板.md',
  'templates/评审报告模板.md',
  'templates/项目看板模板.md',
  'templates/人物卡模板.md',
  'templates/大纲模板.md',
  'templates/后台任务指南.md',
  'modules/writer-module.md',
  'modules/reviewer-module.md',
  'modules/coordinator-module.md',
];

// 需要创建的空目录
const REQUIRED_DIRS = [
  'rules',
  'templates',
  'modules',
  'writing-archive',
  'memory/projects',
  'memory/daily',
];

/**
 * 初始化工作区 - 自动检查并创建缺失文件
 * @param {string} workspacePath - 工作区路径（默认为当前目录）
 * @returns {Promise<void>}
 */
async function initWorkspace(workspacePath = process.cwd()) {
  try {
    console.log(`[writing-mode] 检查工作区配置: ${workspacePath}`);

    // 1. 创建必要目录
    for (const dir of REQUIRED_DIRS) {
      const dirPath = path.join(workspacePath, dir);
      try {
        await fs.access(dirPath);
      } catch {
        await fs.mkdir(dirPath, { recursive: true });
        console.log(`[writing-mode] 创建目录: ${dir}`);
      }
    }

    // 2. 检查并创建缺失文件
    const missingFiles = [];

    for (const file of REQUIRED_FILES) {
      const filePath = path.join(workspacePath, file);
      try {
        await fs.access(filePath);
      } catch {
        missingFiles.push(file);
      }
    }

    if (missingFiles.length === 0) {
      console.log(`[writing-mode] 配置完整，无需初始化`);
      return;
    }

    console.log(`[writing-mode] 发现缺失文件: ${missingFiles.length}个`);

    // 3. 从 scaffold 复制缺失文件
    for (const file of missingFiles) {
      const srcPath = path.join(SCAFFOLD_DIR, file);
      const destPath = path.join(workspacePath, file);

      try {
        await fs.access(srcPath);
        await fs.copyFile(srcPath, destPath);
        console.log(`[writing-mode] 创建文件: ${file}`);
      } catch (err) {
        console.log(`[writing-mode] 警告: 无法从 scaffold 复制 ${file}: ${err.message}`);
      }
    }

    console.log(`[writing-mode] 工作区初始化完成 ✅`);

  } catch (error) {
    console.error(`[writing-mode] 初始化失败: ${error.message}`);
    throw error;
  }
}

// 导出函数供 skill 调用
module.exports = { initWorkspace };

// 如果直接执行，进行初始化
if (require.main === module) {
  const workspacePath = process.argv[2] || process.cwd();
  initWorkspace(workspacePath)
    .then(() => console.log('初始化完成'))
    .catch(err => {
      console.error('初始化失败:', err);
      process.exit(1);
    });
}
