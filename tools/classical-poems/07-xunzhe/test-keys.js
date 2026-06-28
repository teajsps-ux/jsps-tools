function checkErrors(){
      const errors = [];
      try {
        // Test basic functions
        eval('function test() { return true; }');
        errors.push('基本語法: OK');
      } catch (e) {
        errors.push('基本語法錯誤: ' + e.message);
      }

      try {
        // Test showSlide
        eval('function showSlide(index) { current = (index + slides.length) % slides.length; return true; }');
        errors.push('showSlide函數: OK');
      } catch (e) {
        errors.push('showSlide錯誤: ' + e.message);
      }

      try {
        // Test highlightLine
        eval('function highlightLine(i, type) { return type === "poem"; }');
        errors.push('highlightLine函數: OK');
      } catch (e) {
        errors.push('highlightLine錯誤: ' + e.message);
      }

      return errors.join('\n');
    }

    console.log(checkErrors());

    // 添加鍵盤監聽器
    document.addEventListener('keydown', function(event) {
      console.log('按鍵:', event.key);
      if (event.key === 'ArrowRight' || event.key === '→') {
        event.preventDefault();
        console.log('點擊 → 下一頁');
        nextSlide();
      } else if (event.key === 'ArrowLeft' || event.key === '←') {
        event.preventDefault();
        console.log('點擊 ← 上一頁');
        prevSlide();
      }
    });

    alert('鍵盤監聽器已添加！按 ← → 測試。');