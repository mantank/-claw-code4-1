#!/usr/bin/env node
/**
 * pre_tool_check.js
 * Hook: pre_tool — 工具执行前检查
 * 基于 claw-code hooks.json 权限处理模式
 * 
 * 传入: { tool_name: string, args: object, context: object }
 * 传出: { allowed: boolean, modified_args?: object, reason?: string }
 */

function pre_tool_check(input) {
  const { tool_name, args = {} } = input;

  // 危险工具黑名单（精确匹配）
  const DENY_EXACT = new Set(['rm', 'dd', 'shutdown', 'reboot', 'mkfs']);

  // 危险工具前缀（glob风格）
  const DENY_PREFIX = ['eval(', 'exec(', 'system(', '__import__'];

  const lowered = tool_name.toLowerCase();

  // 检查1: 精确匹配
  if (DENY_EXACT.has(lowered)) {
    return {
      allowed: false,
      reason: `危险工具禁止执行: ${tool_name}`
    };
  }

  // 检查2: 前缀匹配
  for (const prefix of DENY_PREFIX) {
    if (lowered.startsWith(prefix) || lowered.includes(prefix.toLowerCase())) {
      return {
        allowed: false,
        reason: `危险模式检测: ${tool_name} 匹配 ${prefix}*`
      };
    }
  }

  // 检查3: 参数中的危险内容
  const args_str = JSON.stringify(args).toLowerCase();
  if (args_str.includes('--no-preserve-root') || args_str.includes('| shred')) {
    return {
      allowed: false,
      reason: `危险参数检测: ${args_str}`
    };
  }

  return { allowed: true };
}

// Node.js CLI 接口
const input = JSON.parse(process.argv[2] || '{}');
const result = pre_tool_check(input);
console.log(JSON.stringify(result));
