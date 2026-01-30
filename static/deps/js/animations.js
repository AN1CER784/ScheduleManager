(() => {
	const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	window.addEventListener('DOMContentLoaded', () => {
		document.body.classList.add('is-loaded');

		// Добавим reveal на детей mainContent, если не расставлено
		const main = document.getElementById('mainContent');
		if (main) {
			Array.from(main.children).forEach(el => {
				if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', '');
			});
		}

		setupScrollReveal();
		setupNavbarShadow();
		setupRecentList();
		setupCounters(); // анимация чисел в hero

		if (!prefersReduced) {
			setupParallaxBlobs();
			setupRipple();
		}
	});

	function setupNavbarShadow() {
		const nav = document.querySelector('header .navbar');
		if (!nav) return;
		const onScroll = () => {
			if (window.scrollY > 4) nav.classList.add('is-scrolled');
			else nav.classList.remove('is-scrolled');
		};
		onScroll();
		window.addEventListener('scroll', onScroll, {passive: true});
	}

	function setupScrollReveal() {
	const items = document.querySelectorAll('[data-reveal]');
	if (!items.length) return;

	// Если нет поддержки IO — показываем всё сразу
	if (!('IntersectionObserver' in window)) {
		items.forEach(el => el.classList.add('is-visible'));
		return;
	}

	const io = new IntersectionObserver((entries, obs) => {
		entries.forEach(entry => {
			if (entry.isIntersecting) {
				entry.target.classList.add('is-visible');
				obs.unobserve(entry.target);
			}
		});
	}, {
		rootMargin: '0px 0px -2% 0px', // проще «достучаться» до нижней кромки
		threshold: 0.01
	});

	items.forEach(el => io.observe(el));

	// Fallback: через 1.2s всё, что не раскрылось, показать
	window.addEventListener('load', () => {
		setTimeout(() => {
			document
				.querySelectorAll('[data-reveal]:not(.is-visible)')
				.forEach(el => el.classList.add('is-visible'));
		}, 1200);
	});
}


	function setupParallaxBlobs() {
		const wrap = document.querySelector('.fx-blobs');
		if (!wrap) return;
		const blobs = wrap.querySelectorAll('.blob');
		if (!blobs.length) return;

		let x = 0, y = 0, tx = 0, ty = 0;
		const damp = 0.08;

		function animate() {
			x += (tx - x) * damp;
			y += (ty - y) * damp;
			blobs.forEach((b, i) => {
				const depth = (i + 1) * 6;
				b.style.transform = `translate3d(${x/depth}%, ${y/depth}%, 0)`;
			});
			requestAnimationFrame(animate);
		}
		animate();

		window.addEventListener('mousemove', (e) => {
			const cx = window.innerWidth / 2;
			const cy = window.innerHeight / 2;
			tx = ((e.clientX - cx) / cx) * 6;
			ty = ((e.clientY - cy) / cy) * 6;
		}, {passive: true});
	}

	function setupRipple() {
		const selector = '.btn, .nav-link';
		document.body.addEventListener('click', (e) => {
			const target = e.target.closest(selector);
			if (!target) return;

			const rect = target.getBoundingClientRect();
			const circle = document.createElement('span');
			const size = Math.max(rect.width, rect.height);
			const x = e.clientX - rect.left - size / 2;
			const y = e.clientY - rect.top - size / 2;

			circle.style.position = 'absolute';
			circle.style.left = `${x}px`;
			circle.style.top = `${y}px`;
			circle.style.width = circle.style.height = `${size}px`;
			circle.style.borderRadius = '50%';
			circle.style.pointerEvents = 'none';
			circle.style.background = 'radial-gradient(circle, rgba(255,255,255,.25) 0%, rgba(255,255,255,0) 60%)';
			circle.style.transform = 'scale(0.2)';
			circle.style.opacity = '0.7';
			circle.style.transition = 'transform .6s ease, opacity .6s ease';
			circle.className = 'ripple-effect';

			const cs = getComputedStyle(target);
			if (cs.position === 'static') target.style.position = 'relative';
			target.appendChild(circle);

			requestAnimationFrame(() => {
				circle.style.transform = 'scale(1)';
				circle.style.opacity = '0';
			});
			setTimeout(() => circle.remove(), 650);
		});
	}

	// Заполняем «Recent items» после небольшой задержки (имитация загрузки)
	function setupRecentList() {
		const ul = document.getElementById('recentItems');
		if (!ul) return;
		setTimeout(() => {
			ul.innerHTML = '';
			const data = [
				{ icon: 'calendar-range.svg', text: 'Событие: Демо спринта — Пт, 16:00' },
				{ icon: 'list-ul.svg', text: 'Проект: Маркетплейс — 12 открытых задач' },
				{ icon: 'list-columns-reverse.svg', text: 'Отчёт: Неделя 36 — доступен' },
			];
			data.forEach(item => {
				const li = document.createElement('li');
				const img = document.createElement('img');
				img.src = `${window.STATIC_URL || '/static/'}deps/icons/${item.icon}`;
				img.width = 16; img.height = 16; img.alt = '';
				li.appendChild(img);
				const span = document.createElement('span');
				span.textContent = item.text;
				li.appendChild(span);
				ul.appendChild(li);
			});
		}, 450);
	}

	// Анимация чисел (hero counters)
	function setupCounters() {
		const nums = document.querySelectorAll('[data-counter]');
		if (!nums.length) return;

		const animate = (el) => {
			const target = parseInt(el.getAttribute('data-target'), 10) || 0;
			const dur = 900;
			const start = performance.now();
			function tick(now) {
				const p = Math.min(1, (now - start) / dur);
				const eased = p < .5 ? 2*p*p : -1 + (4 - 2*p) * p; // easeInOutQuad
				el.textContent = Math.round(target * eased);
				if (p < 1) requestAnimationFrame(tick);
			}
			requestAnimationFrame(tick);
		};

		// Стартовать только когда hero видим
		const first = nums[0];
		if (!('IntersectionObserver' in window)) {
			nums.forEach(animate);
			return;
		}
		const io = new IntersectionObserver((entries, obs) => {
			entries.forEach(entry => {
				if (entry.isIntersecting) {
					nums.forEach(animate);
					obs.disconnect();
				}
			});
		}, { threshold: 0.25 });
		io.observe(first);
	}
})();
