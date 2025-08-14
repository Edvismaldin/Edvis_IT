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

function eventAdminCard(e){
	return `
		<div class="card">
			<div class="flex-between">
				<h3 style="margin:0">${e.title}</h3>
				<div>
					<button class="btn-delete" data-id="${e.id}">Excluir</button>
				</div>
			</div>
			<div class="grid" style="margin-top:8px">
				<div><strong>Início:</strong> ${formatDateTime(e.start_datetime)}</div>
				<div><strong>Fim:</strong> ${formatDateTime(e.end_datetime)}</div>
				<div><strong>Local:</strong> ${e.location || '-'}</div>
				<div><strong>Capacidade:</strong> ${e.capacity} (Vagas: ${e.seats_available})</div>
			</div>
			<p>${e.description || ''}</p>
			<div>
				<button class="btn-view-registrations" data-id="${e.id}">Ver inscrições</button>
			</div>
			<div class="registrations" id="registrations-${e.id}" style="margin-top:8px"></div>
		</div>
	`;
}

async function checkAuth(){
	const state = await fetchJSON('/api/auth.php');
	document.getElementById('login-section').classList.toggle('hidden', state.is_admin);
	document.getElementById('admin-section').classList.toggle('hidden', !state.is_admin);
	if (state.is_admin) {
		loadAdminEvents();
	}
}

async function loadAdminEvents(){
	const data = await fetchJSON('/api/events.php');
	const container = document.getElementById('events-admin');
	container.innerHTML = data.events.map(eventAdminCard).join('');
	container.querySelectorAll('.btn-delete').forEach(btn=>{
		btn.addEventListener('click', async ()=>{
			if(!confirm('Tem certeza que deseja excluir este evento?')) return;
			const id = Number(btn.dataset.id);
			try{
				await fetchJSON('/api/events.php?id='+id, {method:'DELETE'});
				await loadAdminEvents();
			}catch(e){alert(e.message)}
		});
	});
	container.querySelectorAll('.btn-view-registrations').forEach(btn=>{
		btn.addEventListener('click', async ()=>{
			const id = Number(btn.dataset.id);
			const target = document.getElementById('registrations-'+id);
			target.innerHTML = 'Carregando...';
			try{
				const data = await fetchJSON('/api/registrations.php?event_id='+id);
				if (data.registrations.length === 0) {
					target.innerHTML = '<em>Nenhuma inscrição</em>';
					return;
				}
				target.innerHTML = '<div class="card">'+data.registrations.map(r=>`<div><strong>${r.name}</strong> &lt;${r.email}&gt; — ${formatDateTime(r.created_at)}</div>`).join('')+'</div>';
			}catch(e){
				target.innerHTML = '<span style="color:#b00">'+e.message+'</span>';
			}
		});
	});
}

// Login form
document.getElementById('login-form').addEventListener('submit', async (ev)=>{
	ev.preventDefault();
	const password = document.getElementById('password').value;
	try{
		await fetchJSON('/api/auth.php', {method:'POST', body: JSON.stringify({password})});
		await checkAuth();
	}catch(e){ alert(e.message); }
});

// Logout
const logoutBtn = document.getElementById('logout-btn');
logoutBtn.addEventListener('click', async ()=>{
	try{
		await fetchJSON('/api/auth.php?action=logout', {method:'POST'});
		await checkAuth();
	}catch(e){alert(e.message)}
});

// Create event
const eventForm = document.getElementById('event-form');
eventForm.addEventListener('submit', async (ev)=>{
	ev.preventDefault();
	const payload = {
		title: document.getElementById('title').value,
		description: document.getElementById('description').value,
		location: document.getElementById('location').value,
		start_datetime: document.getElementById('start_datetime').value.replace('T',' '),
		end_datetime: document.getElementById('end_datetime').value.replace('T',' '),
		capacity: Number(document.getElementById('capacity').value)
	};
	try{
		await fetchJSON('/api/events.php', {method:'POST', body: JSON.stringify(payload)});
		eventForm.reset();
		await loadAdminEvents();
	}catch(e){alert(e.message)}
});

checkAuth().catch(console.error);