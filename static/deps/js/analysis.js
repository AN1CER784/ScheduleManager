document.querySelectorAll('.analysis-summary').forEach(container => {
	const items = container.querySelectorAll('.accordion-item');

	items.forEach(item => {
		const toggle = item.querySelector('.toggle-summary');
		const body = item.querySelector('.summary-body');

		const rawBlock = item.nextElementSibling?.classList.contains('raw')
			? item.nextElementSibling
			: null;

		const rawHTML = rawBlock?.innerHTML?.trim();

		toggle?.addEventListener('click', () => {
			body.classList.toggle('open');
			toggle.classList.toggle('open');
		});

		if (rawHTML && body) {
			const tempDiv = document.createElement('div');
			tempDiv.innerHTML = rawHTML;
			const raw = tempDiv.textContent;

			const parts = raw.split(/(?:\*\*)?\[\s*(\d+\.\s*[^\]]+)\s*\](?:\*\*)?/).slice(1);

			for (let i = 0; i < parts.length; i += 2) {
				const title = parts[i]?.trim();
				const content = parts[i + 1]?.trim();

				if (!title || !content) continue;

				const detail = document.createElement('details');
				if (i === 0) detail.open = true;

				const summary = document.createElement('summary');
				summary.textContent = title;
				detail.appendChild(summary);

				const div = document.createElement('div');
				div.className = 'section-body text-muted fs-6';
				div.innerHTML = content
					.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
					.replace(/\r?\n/g, '<br>');
				detail.appendChild(div);

				body.appendChild(detail);
			}
		}
	});
});
