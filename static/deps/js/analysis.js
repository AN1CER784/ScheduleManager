 document.querySelectorAll('.analysis-summary').forEach(container => {
            const toggle = container.querySelector('.toggle-summary');
            const body = container.querySelector('.summary-body');
            const rawBlock = container.querySelector('.raw');
            const rawHTML = rawBlock?.innerHTML?.trim();

            // Аккордеон
            toggle?.addEventListener('click', () => {
                body.classList.toggle('open');
                toggle.classList.toggle('open');
            });

            // Парсинг
            if (rawHTML) {
                // Удаляем внешние теги <p>, если есть
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = rawHTML;
                const raw = tempDiv.textContent;

                const parts = raw.split(/(?:\*\*)?\[\s*(\d+\.\s*[^\]]+)\s*\](?:\*\*)?/).slice(1);

                for (let i = 0; i < parts.length; i += 2) {
                    const title = parts[i].trim();
                    const content = parts[i + 1].trim();

                    const detail = document.createElement('details');
                    if (i === 0) detail.open = true;

                    const summary = document.createElement('summary');
                    summary.textContent = title;
                    detail.appendChild(summary);

                    const div = document.createElement('div');
                    div.className = 'section-body text-muted';
                    div.innerHTML = content
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\r?\n/g, '<br>');
                    detail.appendChild(div);

                    body.appendChild(detail);
                }
            }
        });