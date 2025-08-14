<?php
declare(strict_types=1);

require __DIR__ . '/_bootstrap.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
	$data = readJsonBody();
	$eventId = (int)($data['event_id'] ?? 0);
	$name = trim((string)($data['name'] ?? ''));
	$email = trim((string)($data['email'] ?? ''));

	if ($eventId <= 0 || $name === '' || $email === '') {
		jsonResponse(422, ['error' => 'Dados inválidos']);
	}

	$stmt = $pdo->prepare('SELECT id, capacity FROM events WHERE id = ?');
	$stmt->execute([$eventId]);
	$event = $stmt->fetch(PDO::FETCH_ASSOC);
	if (!$event) {
		jsonResponse(404, ['error' => 'Evento não encontrado']);
	}

	$stmt = $pdo->prepare('SELECT COUNT(1) AS c FROM registrations WHERE event_id = ?');
	$stmt->execute([$eventId]);
	$count = (int)$stmt->fetchColumn();
	if ($count >= (int)$event['capacity']) {
		jsonResponse(409, ['error' => 'Evento lotado']);
	}

	try {
		$stmt = $pdo->prepare('INSERT INTO registrations (event_id, name, email, created_at) VALUES (?, ?, ?, ?)');
		$stmt->execute([$eventId, $name, $email, nowIso()]);
	} catch (PDOException $e) {
		if ($e->getCode() === '23000') {
			jsonResponse(409, ['error' => 'Você já está inscrito neste evento']);
		}
		throw $e;
	}

	jsonResponse(201, ['ok' => true]);
}

if ($method === 'GET') {
	if (!isAdmin()) {
		jsonResponse(401, ['error' => 'Não autorizado']);
	}
	$eventId = isset($_GET['event_id']) ? (int)$_GET['event_id'] : 0;
	if ($eventId > 0) {
		$stmt = $pdo->prepare('SELECT id, event_id, name, email, created_at FROM registrations WHERE event_id = ? ORDER BY created_at DESC');
		$stmt->execute([$eventId]);
		$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
		jsonResponse(200, ['registrations' => $rows]);
	} else {
		$stmt = $pdo->query('SELECT id, event_id, name, email, created_at FROM registrations ORDER BY created_at DESC');
		$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
		jsonResponse(200, ['registrations' => $rows]);
	}
}

jsonResponse(405, ['error' => 'Método não permitido']);