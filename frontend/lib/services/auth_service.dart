import 'dart:convert';
import 'dart:developer';
import 'package:http/http.dart' as http;

class AuthService {
  static const String baseUrl = 'http://127.0.0.1:8000/api'; // testing url

  static Future<http.Response> login(String username, String password) {
    return http.post(
      Uri.parse('$baseUrl/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );
  }

  static Future<http.Response> register(
    String username,
    String email,
    String password,
  ) {
    print(
      jsonEncode({'username': username, 'email': email, 'password': password}),
    );
    return http.post(
      Uri.parse('$baseUrl/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
      }),
    );
  }
}
