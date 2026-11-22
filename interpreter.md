---
layout: null
permalink: /interpreter/
---
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="브라우저에서 쓴랭 코드를 작성하고 실행하세요.">
  <title>쓴랭 인터프리터</title>
  <link rel="icon" href="../sseun-pagetti.webp">
  <style>
    :root {
      color-scheme: dark;
      --background: #101412;
      --panel: #181e1b;
      --surface: #111713;
      --border: #344139;
      --text: #f1f5ef;
      --muted: #a7b7ab;
      --accent: #caf48c;
      --error: #ffaaa0;
      font-family: system-ui, sans-serif;
    }
    * { box-sizing: border-box; }
    body { margin: 0; color: var(--text); background: var(--background); }
    main { width: min(1120px, calc(100% - 36px)); margin: 0 auto; padding: clamp(28px, 6vw, 76px) 0 40px; }
    header { display: flex; align-items: end; justify-content: space-between; gap: 20px; flex-wrap: wrap; margin-bottom: 26px; }
    h1 { margin: 0; font-size: clamp(2.25rem, 6vw, 4.4rem); letter-spacing: -.07em; line-height: 1.05; }
    h1 span { color: var(--accent); }
    .brand { display: flex; align-items: center; gap: clamp(12px, 2vw, 20px); }
    .brand-logo { display: block; width: clamp(64px, 10vw, 104px); height: auto; border-radius: 12px; flex-shrink: 0; }
    header p, .hint { color: var(--muted); }
    header p { margin: 14px 0 0; }
    .actions { display: flex; flex-wrap: wrap; gap: 8px; }
    button, select {
      border: 1px solid var(--border); border-radius: 8px; padding: 10px 16px;
      font: inherit; font-weight: 700; background: var(--panel); color: var(--text); cursor: pointer;
    }
    select {
      appearance: none; padding-right: 32px;
      background-image: linear-gradient(45deg, transparent 50%, var(--muted) 50%),
        linear-gradient(135deg, var(--muted) 50%, transparent 50%);
      background-position: right 17px center, right 12px center;
      background-size: 5px 5px; background-repeat: no-repeat;
    }
    button:hover:not(:disabled) { border-color: var(--accent); }
    button:disabled { opacity: .45; cursor: default; }
    #run { background: var(--accent); color: #192112; border-color: var(--accent); }
    :focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
    .workspace { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 12px; }
    .panel { min-width: 0; border: 1px solid var(--border); border-radius: 12px; background: var(--panel); }
    .bar { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 6px; padding: 12px 16px; }
    .bar h2, .bar label { margin: 0; font-size: .95rem; font-weight: 700; }
    .file-actions button { padding: 5px 9px; font-size: .875rem; }
    .file-status { flex-basis: 100%; color: var(--muted); font-size: .875rem; overflow-wrap: anywhere; }
    .file-status:empty { display: none; }
    .hint, #status { font-size: .875rem; }
    #status { color: var(--accent); }
    #status.error { color: var(--error); }
    textarea, pre {
      display: block; width: 100%; margin: 0; border: 0; border-top: 1px solid var(--border);
      padding: 16px; color: var(--text); background: var(--surface);
      font: .96rem/1.7 ui-monospace, Consolas, "Malgun Gothic", monospace;
      border-radius: 0 0 11px 11px;
    }
    textarea { resize: vertical; tab-size: 4; }
    .code-editor { display: grid; grid-template-columns: auto minmax(0, 1fr); }
    .line-gutter {
      position: relative; overflow: hidden; width: clamp(3rem, 11vw, 5.5rem);
      border-top: 1px solid var(--border); border-right: 1px solid var(--border);
      border-radius: 0 0 0 11px; background: var(--surface);
    }
    #line-numbers {
      position: absolute; inset: 0 0 auto;
      border: 0; padding: 16px 8px; text-align: right; color: var(--muted);
      font-variant-numeric: tabular-nums; user-select: none;
    }
    #source { border-bottom-left-radius: 0; }
    #source, #output { height: 370px; }
    #output { overflow: auto; white-space: pre-wrap; overflow-wrap: anywhere; }
    #input-panel { margin-top: 12px; }
    #inputs { min-height: 76px; }
    #live-input { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; padding: 12px 16px; }
    #live-input[hidden] { display: none; }
    #input-value { min-width: 0; flex: 1 1 120px; padding: 8px; border: 1px solid var(--border); border-radius: 8px; font: inherit; }
    #input-error { flex-basis: 100%; color: var(--error); }
    #input-error:empty { display: none; }
    details { margin-top: 22px; border-top: 1px solid var(--border); padding-top: 14px; }
    summary { cursor: pointer; color: var(--accent); font-weight: 700; }
    .guide table { width: 100%; margin-top: 12px; border-collapse: collapse; text-align: left; }
    .guide th, .guide td { padding: 8px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }
    .guide thead th { color: var(--text); background: var(--panel); }
    .guide tbody th { width: 32%; font-weight: 500; overflow-wrap: anywhere; }
    .guide td { color: var(--muted); }
    @media (max-width: 720px) {
      .workspace { grid-template-columns: minmax(0, 1fr); }
      #source { height: 295px; }
      #output { height: 190px; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div class="brand">
        <img class="brand-logo" src="../sseun-pagetti.webp" alt="쓴파게티" width="434" height="434">
        <div>
          <h1><span>쓴랭</span> 인터프리터</h1>
          <p>코드를 작성하고 브라우저에서 실행하세요.</p>
        </div>
      </div>
      <div class="actions">
        <select id="example-choice" aria-label="예제 선택">
          <option value="print">숫자와 글 출력</option>
          <option value="blank">빈 프로그램</option>
          <option value="input">입력과 계산</option>
          <option value="condition">0인지 확인하기</option>
          <option value="repeat">세 번 반복하기</option>
          <option value="jump">반복문 중간에 나오기</option>
        </select>
        <button id="example" type="button">예제 불러오기</button>
        <button id="stop" type="button" disabled>중지</button>
        <button id="run" type="button">실행</button>
      </div>
    </header>
    <div class="workspace">
      <section class="panel">
        <div class="bar">
          <label for="source">쓴랭 코드</label>
          <span class="hint">Ctrl / ⌘ + Enter 실행</span>
          <div class="actions file-actions">
            <button id="open-file" type="button">파일 열기</button>
            <button id="save-file" type="button">.sseun 저장</button>
          </div>
          <input id="source-file" type="file" accept=".sseun" hidden>
          <span id="file-status" class="file-status" role="status"></span>
        </div>
        <div class="code-editor">
          <div class="line-gutter" aria-hidden="true"><pre id="line-numbers"></pre></div>
          <textarea id="source" spellcheck="false" wrap="off"></textarea>
        </div>
      </section>
      <section class="panel" aria-labelledby="output-heading">
        <div class="bar"><h2 id="output-heading">출력</h2><span id="status" role="status">실행 대기</span></div>
        <pre id="output" tabindex="0" aria-labelledby="output-heading"></pre>
      </section>
    </div>
    <section class="panel" id="input-panel">
      <div class="bar"><label for="inputs">미리 입력할 값</label><span class="hint" id="input-hint">선택 사항이에요. 비워 두면 실행 중에 입력할 수 있어요.</span></div>
      <textarea id="inputs" rows="2" aria-describedby="input-hint" placeholder="예: 7"></textarea>
      <form id="live-input" hidden>
        <label for="input-value">정수를 입력해 주세요</label>
        <input id="input-value" type="text" autocomplete="off" aria-describedby="input-error">
        <button type="submit">입력</button>
        <span id="input-error" role="status"></span>
      </form>
    </section>
    <details class="guide" open>
      <summary>쓴랭 문법표</summary>
      <table>
        <thead><tr><th scope="col">문법</th><th scope="col">뜻</th></tr></thead>
        <tbody>
          <tr><th scope="row"><code>레전드 시</code></th><td>프로그램 시작. 첫 줄에 써요.</td></tr>
          <tr><th scope="row"><code>아무 맛도 안난다</code></th><td>프로그램 끝. 마지막 줄에 써요.</td></tr>
          <tr><th scope="row">줄바꿈 · <code>~</code></th><td>명령을 한 줄씩 나눠요. 한 줄로 쓸 때는 <code>~</code>를 넣어요.</td></tr>
          <tr><th scope="row"><code>.</code> · <code>,</code></th><td>점은 +1, 쉼표는 −1. <code>..,,,</code>는 −1이에요.</td></tr>
          <tr><th scope="row">공백 · <code>/</code></th><td>공백은 곱하기, <code>/</code>는 나눈 뒤 내림. 섞이면 왼쪽부터 계산해요.</td></tr>
          <tr><th scope="row"><code>쓴...</code></th><td><code>쓴</code>에 3을 저장해요. <code>쓰은</code>, <code>쓰으은</code>에도 같은 방식으로 저장해요.</td></tr>
          <tr><th scope="row"><code>쓴쓴,</code></th><td><code>쓴</code>의 값을 1 줄여요. 1 늘리려면 <code>쓴쓴.</code>을 써요.</td></tr>
          <tr><th scope="row"><code>쓴단?</code></th><td>정수 하나를 <code>쓴</code>에 저장해요. 미리 적은 값이 없으면 입력할 때까지 기다려요.</td></tr>
          <tr><th scope="row"><code>단쓴!</code></th><td><code>쓴</code>에 저장한 숫자를 출력해요. <code>단...!</code>는 3을 출력해요.</td></tr>
          <tr><th scope="row"><code>단"안녕!"!</code></th><td>따옴표 안의 글을 출력해요.</td></tr>
          <tr><th scope="row"><code>단쓴ㅋ</code> · <code>단ㅋ</code></th><td><code>단쓴ㅋ</code>는 숫자에 해당하는 글자를 출력해요. <code>단ㅋ</code>는 줄을 바꿔요.</td></tr>
          <tr><th scope="row"><code>사랑쓴?단...!</code></th><td><code>쓴</code>이 0일 때만 물음표 뒤의 명령을 실행해요.</td></tr>
          <tr><th scope="row"><code>됬....</code></th><td>왼쪽에 표시된 4번째 줄로 이동해요. 한 줄에 <code>~</code>로 명령을 여러 개 쓰면 번호 범위가 표시돼요.</td></tr>
          <tr><th scope="row"><code>화요알...</code> · <code>화요알끝</code></th><td>두 줄 사이를 3번 반복해요. <code>화요알쓴</code>은 <code>쓴</code>의 값만큼 반복해요.</td></tr>
          <tr><th scope="row"><code>심박수!..</code></th><td>프로그램 전체를 끝내고 종료 값 2를 반환해요.</td></tr>
        </tbody>
      </table>
    </details>
  </main>
  <script>
    const brandLogo = document.querySelector(".brand-logo");
    const favicon = document.querySelector('link[rel="icon"]');
    const logoBase = brandLogo.src;
    const logos = [
      { file: "sseun-hwasal.png", alt: "화살 쓴발면" },
      { file: "sseun-gae-jang.png", alt: "쓴개장" },
      { file: "sseun-pagetti.webp", alt: "쓴파게티" }
    ];
    const logoStorageKey = "sseun.lastLogo";
    let currentLogo;
    try {
      currentLogo = sessionStorage.getItem(logoStorageKey);
    } catch {
      // 저장소를 쓸 수 없어도 이번 페이지에서는 아이콘을 바꿔요.
    }
    function changeLogo() {
      const choices = logos.filter(logo => logo.file !== currentLogo);
      const selected = choices[Math.floor(Math.random() * choices.length)];
      const url = new URL(selected.file, logoBase).href;
      currentLogo = selected.file;
      brandLogo.src = favicon.href = url;
      brandLogo.alt = selected.alt;
      try {
        sessionStorage.setItem(logoStorageKey, currentLogo);
      } catch {
        // 저장소를 쓸 수 없을 때는 현재 페이지에서만 선택을 기억해요.
      }
    }
    changeLogo();
    const examples = {
      blank: { code: "레전드 시\n\n아무 맛도 안난다" },
      print: { code: `레전드 시
단"안녕, 쓴랭!"!
단ㅋ
단...!
단ㅋ
아무 맛도 안난다` },
      input: { inputs: "7\n3", code: `레전드 시
쓴단?
쓰은단?
단"두 수의 곱은 "!
단쓴 쓰은!
단ㅋ
아무 맛도 안난다` },
      condition: { inputs: "0", code: `레전드 시
쓴단?
사랑쓴?단"0이에요!"!
사랑쓴?단ㅋ
사랑쓴?심박수!
단"0이 아니에요!"!
단ㅋ
아무 맛도 안난다` },
      repeat: { code: `레전드 시
화요알...
단"안녕!"!
단ㅋ
화요알끝
아무 맛도 안난다` },
      jump: { code: `레전드 시
쓴...
화요알.....
쓴쓴,
단쓴!
단ㅋ
사랑쓴?됬.........
화요알끝
단"반복문 밖이에요!"!
단ㅋ
아무 맛도 안난다` }
    };
    async function runSseun(source, { read, write, signal }) {
      const lines = source.trim().split(/\r?\n|~/);
      if (lines[0] !== "레전드 시" || lines.at(-1) !== "아무 맛도 안난다") {
        throw new Error("첫 줄은 '레전드 시', 마지막 줄은 '아무 맛도 안난다'여야 해요.");
      }
      const variables = new Map();
      const loopEnds = new Map();
      const loopStarts = new Map();
      const openLoops = [];
      const remaining = new Map();
      lines.forEach((line, index) => {
        if (line === "화요알끝") {
          if (!openLoops.length) throw new Error(`${index + 1}번째 줄에 짝이 없는 화요알끝이 있어요.`);
          const start = openLoops.pop();
          loopEnds.set(start, index);
          loopStarts.set(index, start);
        } else if (line.startsWith("화요알")) {
          openLoops.push(index);
        }
      });
      if (openLoops.length) throw new Error(`${openLoops.at(-1) + 1}번째 줄의 화요알에 화요알끝이 필요해요.`);
      function term(text) {
        const match = text.match(/^(쓴|쓰으*은)?([.,]*)$/u);
        if (!match) throw new Error(`잘못된 숫자 표현: ${text}`);
        let value = variables.get(match[1]) ?? 0n;
        for (const sign of match[2]) value += sign === "." ? 1n : -1n;
        return value;
      }
      function number(expression) {
        const parts = expression.split(/( +|\/)/);
        if (parts.length > 1 && parts.some((part, index) => index % 2 === 0 && !part)) {
          throw new Error("곱셈과 나눗셈 기호 양쪽에 값이 필요해요.");
        }
        let value = term(parts[0]);
        for (let index = 1; index < parts.length; index += 2) {
          const right = term(parts[index + 1]);
          if (parts[index] === "/") {
            if (right === 0n) throw new Error("0으로 나눌 수 없어요.");
            const roundDown = value % right !== 0n && (value < 0n) !== (right < 0n);
            value = value / right - (roundDown ? 1n : 0n);
          } else {
            value *= right;
          }
        }
        return value;
      }
      let pc = 1;
      let steps = 0;
      let outputLength = 0;
      function print(text) {
        outputLength += text.length;
        if (outputLength > 100000) throw new Error("웹 실행기의 출력 한도에 도달했어요.");
        write(text);
      }
      while (pc < lines.length - 1) {
        if (++steps % 256 === 0) await new Promise(resolve => setTimeout(resolve, 0));
        if (signal.aborted) throw new Error("실행을 중지했어요.");
        if (steps > 100000) throw new Error(`${pc + 1}번째 줄: 실행 한도에 도달했어요. 반복과 이동을 확인하세요.`);
        if (pc === 0) { pc = 1; continue; }
        try {
          let command = lines[pc];
          if (loopEnds.has(pc)) {
            const expression = command.slice("화요알".length);
            if (!expression) throw new Error("화요알 뒤에 횟수를 써 주세요.");
            const count = number(expression);
            if (count > 0n) {
              remaining.set(pc, count);
              pc++;
            } else {
              pc = loopEnds.get(pc) + 1;
            }
            continue;
          }
          if (loopStarts.has(pc)) {
            const start = loopStarts.get(pc);
            const count = remaining.get(start) ?? 0n;
            if (count > 1n) {
              remaining.set(start, count - 1n);
              pc = start + 1;
            } else {
              remaining.delete(start);
              pc++;
            }
            continue;
          }
          while (command.startsWith("사랑")) {
            const separator = command.indexOf("?");
            if (separator < 0) throw new Error("사랑 뒤에는 조건과 ?가 필요해요.");
            command = number(command.slice(2, separator)) === 0n ? command.slice(separator + 1) : "";
          }
          if (command.startsWith("됬")) {
            const line = number(command.slice(1));
            if (line < 1n || line > BigInt(lines.length)) throw new Error(`이동할 줄이 없어요: ${line}`);
            const target = Number(line) - 1;
            for (const start of remaining.keys()) {
              if (!(start < target && target <= loopEnds.get(start))) remaining.delete(start);
            }
            pc = target;
            continue;
          }
          if (command.startsWith("심박수!")) return number(command.slice("심박수!".length));
          const assignment = command.match(/^(쓴|쓰으*은)(.*)$/u);
          const text = command.match(/^단"([^"]*)"!$/u);
          if (assignment) {
            const [, name, expression] = assignment;
            variables.set(name, expression === "단?" ? await read() : number(expression));
          } else if (text) {
            print(text[1]);
          } else if (command.startsWith("단") && command.endsWith("!")) {
            print(String(number(command.slice(1, -1))));
          } else if (command.startsWith("단") && command.endsWith("ㅋ")) {
            const expression = command.slice(1, -1);
            const code = number(expression);
            if (code < 0n || code > 0x10ffffn) throw new Error("유효한 유니코드 번호를 써 주세요.");
            print(expression ? String.fromCodePoint(Number(code)) : "\n");
          } else if (command) {
            throw new Error(`알 수 없는 명령: ${command}`);
          }
          pc++;
        } catch (error) {
          throw new Error(`${pc + 1}번째 줄: ${error.message}`);
        }
      }
      return 0n;
    }
    const source = document.querySelector("#source");
    const lineNumbers = document.querySelector("#line-numbers");
    const inputs = document.querySelector("#inputs");
    const inputForm = document.querySelector("#live-input");
    const inputValue = document.querySelector("#input-value");
    const inputError = document.querySelector("#input-error");
    const output = document.querySelector("#output");
    const status = document.querySelector("#status");
    const runButton = document.querySelector("#run");
    const stopButton = document.querySelector("#stop");
    const exampleButton = document.querySelector("#example");
    const exampleChoice = document.querySelector("#example-choice");
    const openButton = document.querySelector("#open-file");
    const saveButton = document.querySelector("#save-file");
    const filePicker = document.querySelector("#source-file");
    const fileStatus = document.querySelector("#file-status");
    let controller;
    let loadedCode = examples.print.code;
    let loadedInputs = "";
    let filename = "program.sseun";
    function syncLineScroll() {
      lineNumbers.style.transform = `translateY(${-source.scrollTop}px)`;
    }
    function updateLineNumbers() {
      const text = source.value;
      const trimmed = text.trim();
      const leadingLines = trimmed ? text.slice(0, text.length - text.trimStart().length).split("\n").length - 1 : 0;
      const programRows = trimmed.split(/\r?\n/);
      let nextLine = 1;
      lineNumbers.textContent = text.split(/\r?\n/).map((_, index) => {
        const row = programRows[index - leadingLines];
        if (row === undefined) return "–";
        const first = nextLine;
        nextLine += row.split("~").length;
        return nextLine === first + 1 ? String(first) : `${first}–${nextLine - 1}`;
      }).join("\n");
      syncLineScroll();
    }
    source.value = loadedCode;
    updateLineNumbers();
    source.addEventListener("input", updateLineNumbers);
    source.addEventListener("scroll", syncLineScroll);
    exampleButton.addEventListener("click", () => {
      const edited = source.value !== loadedCode || inputs.value !== loadedInputs;
      if (edited && !confirm("현재 코드와 입력값을 예제로 바꿀까요?")) return;
      const example = examples[exampleChoice.value];
      source.value = loadedCode = example.code;
      updateLineNumbers();
      inputs.value = loadedInputs = example.inputs ?? "";
      filename = "program.sseun";
      fileStatus.textContent = "";
      source.focus();
    });
    openButton.addEventListener("click", () => filePicker.click());
    filePicker.addEventListener("change", async () => {
      const file = filePicker.files[0];
      filePicker.value = "";
      if (!file) return;
      if (!file.name.toLowerCase().endsWith(".sseun")) {
        fileStatus.textContent = ".sseun 파일을 선택해 주세요.";
        return;
      }
      try {
        const text = await file.text();
        if (controller) {
          fileStatus.textContent = "실행을 마친 뒤 파일을 다시 열어 주세요.";
          return;
        }
        if (source.value !== loadedCode && !confirm("편집 중인 코드를 파일 내용으로 바꿀까요?")) return;
        source.value = text;
        updateLineNumbers();
        loadedCode = source.value;
        filename = file.name;
        fileStatus.textContent = `${filename} 열었어요.`;
        source.focus();
      } catch {
        fileStatus.textContent = "파일을 읽을 수 없어요.";
      }
    });
    saveButton.addEventListener("click", () => {
      const file = new Blob([source.value], { type: "text/plain;charset=utf-8" });
      const url = URL.createObjectURL(file);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      fileStatus.textContent = `${filename} 다운로드를 요청했어요.`;
    });
    function parseInput(text) {
      const input = text.trim();
      if (!/^[+-]?[0-9](?:_?[0-9])*$/u.test(input)) throw new Error("입력값은 정수여야 해요.");
      return BigInt(input.replaceAll("_", ""));
    }
    function waitForInput(signal) {
      return new Promise((resolve, reject) => {
        function close() {
          inputForm.hidden = true;
          inputForm.removeEventListener("submit", submit);
          signal.removeEventListener("abort", cancel);
        }
        function cancel() {
          close();
          reject(new Error("실행을 중지했어요."));
        }
        function submit(event) {
          event.preventDefault();
          let value;
          try {
            value = parseInput(inputValue.value);
          } catch (error) {
            inputError.textContent = error.message;
            inputValue.focus();
            return;
          }
          close();
          status.textContent = "실행 중";
          resolve(value);
        }
        if (signal.aborted) {
          cancel();
          return;
        }
        inputValue.value = "";
        inputError.textContent = "";
        inputForm.hidden = false;
        status.textContent = "입력 대기 중";
        inputForm.addEventListener("submit", submit);
        signal.addEventListener("abort", cancel);
        inputValue.focus();
      });
    }
    async function execute() {
      if (controller) return;
      controller = new AbortController();
      runButton.disabled = exampleButton.disabled = exampleChoice.disabled = openButton.disabled = true;
      stopButton.disabled = false;
      status.classList.remove("error");
      status.textContent = "실행 중";
      output.textContent = "";
      const prepared = inputs.value.trimEnd();
      const inputLines = prepared ? prepared.split(/\r?\n/) : [];
      let inputIndex = 0;
      let printed = "";
      try {
        const exitCode = await runSseun(source.value, {
          signal: controller.signal,
          read() {
            if (inputIndex < inputLines.length) return parseInput(inputLines[inputIndex++]);
            output.textContent = printed;
            return waitForInput(controller.signal);
          },
          write(text) { printed += text; }
        });
        status.textContent = `완료 · 종료 값 ${exitCode}`;
      } catch (error) {
        if (controller.signal.aborted) {
          status.textContent = "중지됨";
        } else {
          status.classList.add("error");
          status.textContent = "실행 오류";
          changeLogo();
          if (printed && !printed.endsWith("\n")) printed += "\n";
          printed += error.message;
        }
      } finally {
        output.textContent = printed;
        controller = undefined;
        runButton.disabled = exampleButton.disabled = exampleChoice.disabled = openButton.disabled = false;
        stopButton.disabled = true;
      }
    }
    runButton.addEventListener("click", execute);
    stopButton.addEventListener("click", () => controller?.abort());
    source.addEventListener("keydown", event => {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        execute();
      }
    });
  </script>
</body>
</html>
