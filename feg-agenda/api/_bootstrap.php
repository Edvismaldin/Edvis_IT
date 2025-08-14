<?php
declare(strict_types=1);

if (session_status() === PHP_SESSION_NONE) {
	session_start();
}

// Always return JSON from API endpoints
header('Content-Type: application/json; charset=utf-8');

$baseDir = dirname(__DIR__);
$dataDir = $baseDir . DIRECTORY_SEPARATOR . 'data';
if (!is_dir($dataDir)) {
	mkdir($dataDir, 0777, true);
}
$dbFile = $dataDir . DIRECTORY_SEPARATOR . 'database.sqlite';

try {
	$pdo = new PDO('sqlite:' . $dbFile);
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	$pdo->exec('PRAGMA foreign_keys = ON');
} catch (PDOException $e) {
	http_response_code(500);
	echo json_encode(['error' => 'DB connection failed', 'details' => $e->getMessage()]);
	exit;
}

function migrate(PDO $pdo): void {
	$pdo->exec('CREATE TABLE IF NOT EXISTS events (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		description TEXT,
		location TEXT,
		start_datetime TEXT NOT NULL,
		end_datetime TEXT NOT NULL,
		capacity INTEGER NOT NULL DEFAULT 0,
		created_at TEXT NOT NULL
	)');
	$pdo->exec('CREATE TABLE IF NOT EXISTS registrations (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		event_id INTEGER NOT NULL,
		name TEXT NOT NULL,
		email TEXT NOT NULL,
		created_at TEXT NOT NULL,
		UNIQUE(event_id, email),
		FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE
	)');
}

migrate($pdo);

function nowIso(): string {
	return (new DateTimeImmutable('now'))->format('Y-m-d H:i:s');
}

function readJsonBody(): array {
	$raw = file_get_contents('php://input');
	if ($raw === false || $raw === '') {
		return [];
	}
	$data = json_decode($raw, true);
	return is_array($data) ? $data : [];
}

function jsonResponse(int $statusCode, $data): void {
	http_response_code($statusCode);
	echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
	exit;
}

function isAdmin(): bool {
	return !empty($_SESSION['is_admin']);
}

function requireAdmin(): void {
	if (!isAdmin()) {
		jsonResponse(401, ['error' => 'Não autorizado']);
	}
}

function env(string $key, ?string $default = null): ?string {
	$val = getenv($key);
	return $val !== false ? $val : $default;
}

function getAdminPassword(): string {
	$fromEnv = env('ADMIN_PASSWORD');
	if ($fromEnv !== null && $fromEnv !== '') {
		return $fromEnv;
	}
	return 'admin123';
}