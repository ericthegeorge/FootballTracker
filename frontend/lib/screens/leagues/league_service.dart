import 'dart:convert';
import 'package:http/http.dart' as http;

class LeagueService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  static Future<List<String>> fetchLeagues() async {
    final response = await http.get(Uri.parse('$baseUrl/leagues/'));
    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      return data.map<String>((league) => league['name'].toString()).toList();
    } else {
      throw Exception('Failed to load leagues');
    }
  }

  static Future<bool> addLeague(String name) async {
    final response = await http.post(
      Uri.parse('$baseUrl/leagues/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name}),
    );
    return response.statusCode == 201;
  }

  static Future<bool> deleteLeague(String league) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/leagues/$league'),
      headers: {'Content-Type': 'application/json'},
    );

    return response.statusCode == 204;
  }

  static Future<bool> updateLeague(String oldName, String newName) async {
    final response = await http.put(
      Uri.parse('$baseUrl/leagues/$oldName'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': newName}),
    );

    print(response);
    print(response.statusCode);
    return response.statusCode == 200;
  }
}
