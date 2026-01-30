import * as params from '@params';

let fuse; // 검색 엔진
let resList = document.getElementById('searchResults');
let sInput = document.getElementById('searchInput');
let first, last, current_elem = null
let resultsAvailable = false;

// 검색 인덱스 로드
window.onload = function () {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                let data = JSON.parse(xhr.responseText);
                if (data) {
                    // Fuse.js 옵션 설정 (태그 검색 추가 및 하이라이팅 활성화)
                    let options = {
                        distance: 100,
                        threshold: 0.4,
                        ignoreLocation: true,
                        includeMatches: true, // 하이라이팅을 위한 매치 정보 포함
                        minMatchCharLength: 2,
                        keys: [
                            'title',
                            'tags',   // 태그 검색 추가
                            'summary',
                            'content'
                        ]
                    };
                    fuse = new Fuse(data, options); 
                }
            } else {
                console.log(xhr.responseText);
            }
        }
    };
    xhr.open('GET', "../index.json");
    xhr.send();
}

// 하이라이트 처리 함수
function highlightText(text, indices) {
    if (!indices || indices.length === 0) return text;
    
    let result = '';
    let lastIndex = 0;
    
    indices.forEach(([start, end]) => {
        result += text.substring(lastIndex, start);
        result += `<mark>${text.substring(start, end + 1)}</mark>`; // <mark> 태그로 감싸기
        lastIndex = end + 1;
    });
    
    result += text.substring(lastIndex);
    return result;
}

function activeToggle(ae) {
    document.querySelectorAll('.focus').forEach(function (element) {
        element.classList.remove("focus")
    });
    if (ae) {
        ae.focus()
        document.activeElement = current_elem = ae;
        ae.parentElement.classList.add("focus")
    } else {
        document.activeElement.parentElement.classList.add("focus")
    }
}

function reset() {
    resultsAvailable = false;
    resList.innerHTML = sInput.value = ''; 
    sInput.focus(); 
}

// 검색 실행 로직
sInput.onkeyup = function (e) {
    if (fuse) {
        let results = fuse.search(this.value.trim()); 
        
        if (results.length !== 0) {
            let resultSet = ''; 

            for (let item in results) {
                let post = results[item].item;
                let matches = results[item].matches;
                
                // 제목 하이라이팅 처리
                let titleMatch = matches.find(m => m.key === 'title');
                let displayTitle = titleMatch ? highlightText(post.title, titleMatch.indices) : post.title;

                // 태그 표시 로직
                let tagsHtml = '';
                if(post.tags && post.tags.length > 0){
                    tagsHtml = `<div style="font-size: 0.8rem; color: var(--secondary); margin-top: 5px;">🏷️ ${post.tags.join(', ')}</div>`;
                }

                resultSet += `<li class="post-entry" style="padding: 10px; margin-bottom: 5px;">` +
                             `<header class="entry-header" style="font-weight: bold;">${displayTitle}&nbsp;»</header>` +
                             `${tagsHtml}` +
                             `<a href="${post.permalink}" aria-label="${post.title}"></a>` +
                             `</li>`;
            }

            resList.innerHTML = resultSet;
            resultsAvailable = true;
            first = resList.firstChild;
            last = resList.lastChild;
        } else {
            resultsAvailable = false;
            resList.innerHTML = '';
        }
    }
}

sInput.addEventListener('search', function (e) {
    if (!this.value) reset()
})

document.onkeydown = function (e) {
    let key = e.key;
    let ae = document.activeElement;
    let inbox = document.getElementById("searchbox").contains(ae)

    if (ae === sInput) {
        let elements = document.getElementsByClassName('focus');
        while (elements.length > 0) elements[0].classList.remove('focus');
    } else if (current_elem) ae = current_elem;

    if (key === "Escape") {
        reset()
    } else if (!resultsAvailable || !inbox) {
        return
    } else if (key === "ArrowDown") {
        e.preventDefault();
        if (ae == sInput) activeToggle(resList.firstChild.lastChild);
        else if (ae.parentElement != last) activeToggle(ae.parentElement.nextSibling.lastChild);
    } else if (key === "ArrowUp") {
        e.preventDefault();
        if (ae.parentElement == first) activeToggle(sInput);
        else if (ae != sInput) activeToggle(ae.parentElement.previousSibling.lastChild);
    } else if (key === "ArrowRight") {
        ae.click();
    }
}