<?php
declare(strict_types=1);

require __DIR__ . '/_bootstrap.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'GET') {
	$from = $_GET['from'] ?? null;
	$to = $_GET['to'] ?? null;

	$sql = 'SELECT e.*,
		(e.capacity - IFNULL((SELECT COUNT(1) FROM registrations r WHERE r.event_id = e.id), 0)) AS seats_available,
		IFNULL((SELECT COUNT(1) FROM registrations r2 WHERE r2.event_id = e.id), 0) AS seats_taken
		FROM events e';
	$conds = [];
	$params = [];
	if ($from) {
		$conds[] = 'e.start_datetime >= ?';
		$params[] = $from;
	}
	if ($to) {
		$conds[] = 'e.end_datetime <= ?';
		$params[] = $to;
	}
	if (!empty($conds)) {
		$sql .= ' WHERE ' . implode(' AND ', $conds);
	}
	$sql .= ' ORDER BY e.start_datetime ASC';

	$stmt = $pdo->prepare($sql);
	$stmt->execute($params);
	$events = $stmt->fetchAll(PDO::FETCH_ASSOC);
	jsonResponse(200, ['events' => $events]);
}

if ($method === 'POST') {
	requireAdmin();
	$data = readJsonBody();
	$title = trim((string)($data['title'] ?? ''));
	$description = trim((string)($data['description'] ?? ''));
	$location = trim((string)($data['location'] ?? ''));
	$start = trim((string)($data['start_datetime'] ?? ''));
	$end = trim((string)($data['end_datetime'] ?? ''));
	$capacity = (int)($data['capacity'] ?? 0);

	if ($title === '' || $start === '' || $end === '' || $capacity < 0) {
		jsonResponse(422, ['error' => 'Dados inválidos']);
	}

	$stmt = $pdo->prepare('INSERT INTO events (title, description, location, start_datetime, end_datetime, capacity, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)');
	$stmt->execute([$title, $description, $location, $start, $end, $capacity, nowIso()]);

	$id = (int)$pdo->lastInsertId();
	$stmt2 = $pdo->prepare('SELECT e.*,
		(e.capacity - IFNULL((SELECT COUNT(1) FROM registrations r WHERE r.event_id = e.id), 0)) AS seats_available,
		IFNULL((SELECT COUNT(1) FROM registrations r2 WHERE r2.event_id = e.id), 0) AS seats_taken
		FROM events e WHERE e.id = ?');
	$stmt2->execute([$id]);
	$event = $stmt2->fetch(PDO::FETCH_ASSOC);
	jsonResponse(201, ['event' => $event]);
}

if ($method === 'PUT') {
	requireAdmin();
	$data = readJsonBody();
	$id = (int)($data['id'] ?? 0);
	if ($id <= 0) {
		jsonResponse(422, ['error' => 'ID inválido']);
	}
	$fields = [];
	$params = [];
	foreach (['title','description','location','start_datetime','end_datetime','capacity'] as $field) {
		if (array_key_exists($field, $data)) {
			$fields[] = "$field = ?";
			if ($field === 'capacity') {
				$params[] = (int)$data[$field];
			} else {
				$params[] = (string)$data[$field];
			}
		}
	}
	if (empty($fields)) {
		jsonResponse(422, ['error' => 'Nada para atualizar']);
	}
	$params[] = $id;
	$sql = 'UPDATE events SET ' . implode(', ', $fields) . ' WHERE id = ?';
	$stmt = $pdo->prepare($sql);
	$stmt->execute($params);
	jsonResponse(200, ['ok' => true]);
}

if ($method === 'DELETE') {
	requireAdmin();
	$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
	if ($id <= 0) {
		jsonResponse(422, ['error' => 'ID inválido']);
	}
	$stmt = $pdo->prepare('DELETE FROM events WHERE id = ?');
	$stmt->execute([$id]);
	jsonResponse(200, ['ok' => true]);
}

jsonResponse(405, ['error' => 'Método não permitido']);