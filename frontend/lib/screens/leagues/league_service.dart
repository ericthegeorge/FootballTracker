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
}
