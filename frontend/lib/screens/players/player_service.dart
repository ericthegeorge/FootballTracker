import 'dart:convert';
import 'package:http/http.dart' as http;

class PlayerService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  static Future<List<String>> fetchPlayers() async {
    final response = await http.get(Uri.parse('$baseUrl/players/'));
    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      return data.map<String>((players) => players['name'].toString()).toList();
    } else {
      throw Exception('Failed to load players');
    }
  }

  static Future<bool> addPlayer(String name) async {
    final response = await http.post(
      Uri.parse('$baseUrl/players/'),
      headers: {'Content-type': 'applications/json'},
      body: jsonEncode({'name': name}),
    );
    return response.statusCode == 201;
  }

  static Future<bool> deletePlayer(String player) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/players/$player'),
      headers: {'Content-Type': 'application/json'},
    );

    return response.statusCode == 204;
  }

  static Future<bool> updatePlayer(String oldName, String newName) async {
    final response = await http.put(
      Uri.parse('$baseUrl/players/$oldName'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': newName}),
    );

    print(response);
    print(response.statusCode);
    return response.statusCode == 200;
  }
  
}