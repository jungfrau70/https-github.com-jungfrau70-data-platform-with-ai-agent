#!/bin/bash

# SSH agent 설정 (SSH 키가 있는 경우에만)
if [ -f ~/.ssh/inhwan_jung_key ]; then
    if ! ssh-add -l &>/dev/null; then
        echo "🔑 SSH agent에 키 추가 중..."
        eval "$(ssh-agent -s)" &>/dev/null
        ssh-add ~/.ssh/inhwan_jung_key &>/dev/null
    fi
else
    echo "ℹ️  SSH 키를 찾을 수 없습니다. HTTPS 인증을 사용합니다."
    echo "   Personal Access Token이 필요할 수 있습니다."
fi

# Git 상태 확인
echo "🔍 Git 상태 확인 중..."
git status

# 변경사항 추가
echo "📝 변경사항 추가 중..."
git add .

# 변경된 파일 목록 가져오기 (첫 번째 파일만)
CHANGED_FILES=$(git diff --cached --name-only | head -1)
if [ -n "$CHANGED_FILES" ]; then
    CHANGED_FILES=" - $CHANGED_FILES"
    if [ $(git diff --cached --name-only | wc -l) -gt 1 ]; then
        CHANGED_FILES="${CHANGED_FILES} and $(($(git diff --cached --name-only | wc -l) - 1)) more files"
    fi
else
    CHANGED_FILES=""
fi

# 커밋 메시지 생성
COMMIT_MSG="Update: $(date +"%Y-%m-%d %H:%M:%S")${CHANGED_FILES}"
echo "💾 커밋 중: $COMMIT_MSG"
if git commit -m "$COMMIT_MSG"; then
    echo "✅ 커밋 완료"
else
    echo "ℹ️  커밋할 변경사항이 없습니다 (이미 커밋됨)"
fi

# # 푸시 실행
# echo "🚀 푸시 중..."
# # git push origin main
# if git push -u origin feature/streamlit 2>&1; then
#     echo "✅ 푸시 완료"
# else
#     echo "❌ 푸시 실패"
#     echo ""
#     echo "💡 해결 방법:"
#     echo "   1. HTTPS 사용 시: GitHub Personal Access Token 설정 필요"
#     echo "   2. SSH 사용 시: SSH 키 생성 및 GitHub에 등록 필요"
#     echo "   3. 원격 저장소 URL 확인: git remote -v"
#     exit 1
# fi
# git push origin main
# 푸시 실행 (일반 push 먼저 시도)
echo "🚀 푸시 중..."
# if git push origin feature/hybrid-optimizer 2>&1; then
if git push origin master 2>&1; then
    echo "✅ 푸시 완료"
else
    PUSH_ERROR=$?
    echo "⚠️  일반 푸시 실패 (exit code: $PUSH_ERROR)"
    # 히스토리 재작성 후 force push 필요 시도
    echo "🔄 원격 브랜치 상태 확인 중..."
    git fetch origin feature/hybrid-optimizer 2>&1 || true
    echo "🔄 히스토리 재작성으로 인한 force push 시도 중..."
    if git push --force-with-lease origin feature/hybrid-optimizer 2>&1; then
        echo "✅ Force push 완료"
    else
        FORCE_LEASE_ERROR=$?
        echo "⚠️  --force-with-lease 실패 (exit code: $FORCE_LEASE_ERROR)"
        echo "💡 히스토리 재작성으로 인해 원격 브랜치 상태가 예상과 다릅니다."
        echo "🔄 --force 옵션으로 강제 push 시도 중... (주의: 원격 브랜치를 덮어씁니다)"
        if git push --force origin feature/hybrid-optimizer 2>&1; then
            echo "✅ Force push 완료"
        else
            echo "❌ Force push도 실패했습니다"
            echo ""
            echo "💡 해결 방법:"
            echo "   1. HTTPS 사용 시: GitHub Personal Access Token 설정 필요"
            echo "   2. SSH 사용 시: SSH 키 생성 및 GitHub에 등록 필요"
            echo "   3. 수동 실행: git push --force origin feature/hybrid-optimizer"
            exit 1
        fi
    fi
fi

echo "✅ 완료!"
