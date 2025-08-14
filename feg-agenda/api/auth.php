<?php
declare(strict_types=1);

require __DIR__ . '/_bootstrap.php';

$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';

if ($method === 'GET') {
	jsonResponse(200, ['is_admin' => isAdmin()]);
}

if ($method === 'POST') {
	if ($action === 'logout') {
		$_SESSION = [];
		if (ini_get('session.use_cookies')) {
			$params = session_get_cookie_params();
			setcookie(session_name(), '', time() - 42000,
				$params['path'], $params['domain'],
				$params['secure'], $params['httponly']
			);
		}
		session_destroy();
		jsonResponse(200, ['ok' => true]);
	}
	
	$data = readJsonBody();
	$password = $data['password'] ?? '';
	if ($password === getAdminPassword()) {
		$_SESSION['is_admin'] = true;
		jsonResponse(200, ['ok' => true, 'is_admin' => true]);
	} else {
		jsonResponse(401, ['error' => 'Senha inválida']);
	}
}

jsonResponse(405, ['error' => 'Método não permitido']);