// 測試對照頁亮燈
    function testHighlight() {
      console.log('=== 測試 highlightLine 函數 ===');
      const debugLog = [];

      try {
        // 測試 clearHighlights
        debugLog.push('測試 clearHighlights...');
        document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active'));
        debugLog.push('✓ clearHighlights 完成');

        // 測試 highlightLine (poem模式)
        debugLog.push('測試 highlightLine (poem模式)...');
        const poems = document.querySelectorAll('.poem-row[data-pair="0"]');
        const plains = document.querySelectorAll('.plain-row[data-pair="0"]');
        document.querySelectorAll('.plain-row').forEach(r => r.classList.remove('active'));
        poems.forEach(r => r.classList.add('active'));
        debugLog.push('✓ poem模式亮燈成功，元素數量: ' + poems.length);

        // 測試 highlightLine (plain模式)
        debugLog.push('測試 highlightLine (plain模式)...');
        document.querySelectorAll('.poem-row').forEach(r => r.classList.remove('active'));
        plains.forEach(r => r.classList.add('active'));
        debugLog.push('✓ plain模式亮燈成功，元素數量: ' + plains.length);

        // 測試 highlightLine (compare模式)
        debugLog.push('測試 highlightLine (compare模式)...');
        poems.forEach(r => r.classList.add('active'));
        plains.forEach(r => r.classList.add('active'));
        debugLog.push('✓ compare模式亮燈成功');

      } catch (e) {
        debugLog.push('✗ 錯誤: ' + e.message);
      }

      return debugLog.join('\n');
    }

    console.log(testHighlight());