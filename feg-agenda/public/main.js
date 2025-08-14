async function fetchJSON(url, options={}){
	const res = await fetch(url, Object.assign({headers:{'Content-Type':'application/json'}}, options));
	if(!res.ok){
		const err = await res.json().catch(()=>({error:'Erro desconhecido'}));
		throw new Error(err.error || 'Erro');
	}
	return res.json();
}

function formatDateTime(iso){
	if(!iso) return '';
	const d = new Date(iso.replace(' ', 'T'));
	return d.toLocaleString('pt-BR');
}

function eventCard(e){
	const available = Number(e.seats_available);
	const full = available <= 0;
	return `
		<div class="card event">
			<div class="meta">
				<div><strong>${formatDateTime(e.start_datetime)} - ${formatDateTime(e.end_datetime)}</strong></div>
				<div>${e.location ? e.location : ''}</div>
				<div>Vagas: ${available} / ${e.capacity} ${full ? '<span class="tag">Lotado</span>' : ''}</div>
			</div>
			<div class="content" style="flex:1">
				<h3 style="margin-top:0">${e.title}</h3>
				<p>${e.description ? e.description : ''}</p>
				${full ? '' : `
				<form class="register-form" data-event-id="${e.id}">
					<div class="grid">
						<input type="text" name="name" placeholder="Seu nome" required />
						<input type="email" name="email" placeholder="Seu e-mail" required />
					</div>
					<button type="submit">Inscrever-se</button>
				</form>`}
			</div>
		</div>
	`;
}

async function loadEvents(){
	const data = await fetchJSON('/api/events.php');
	const container = document.getElementById('events');
	container.innerHTML = data.events.map(eventCard).join('');
	container.querySelectorAll('form.register-form').forEach(form => {
		form.addEventListener('submit', async (ev) => {
			ev.preventDefault();
			const eventId = Number(form.dataset.eventId);
			const formData = new FormData(form);
			const payload = {
				event_id: eventId,
				name: formData.get('name'),
				email: formData.get('email')
			};
			form.querySelector('button').disabled = true;
			try {
				await fetchJSON('/api/registrations.php', {method:'POST', body: JSON.stringify(payload)});
				alert('Inscrição realizada com sucesso!');
				await loadEvents();
			} catch (e) {
				alert(e.message);
			} finally {
				form.querySelector('button').disabled = false;
			}
		});
	});
}

loadEvents().catch(err=>{
	console.error(err);
	alert('Falha ao carregar eventos');
});