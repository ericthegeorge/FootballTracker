import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://127.0.0.1:8000/api";

  Future<http.Response> login(String username, String password) async {
    final url = Uri.parse('$baseUrl/user/$username/login/');
    final response = await http.post(
      url,
      body: {'password': password},
    );
    return response;
  }

  Future<http.Response> register(String username, String password) async {
    final url = Uri.parse('$baseUrl/user/$username/register/');
    final response = await http.post(
      url,
      body: {'password': password},
    );
    return response;
  }
}
