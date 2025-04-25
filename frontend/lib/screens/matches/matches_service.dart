import 'dart:convert';
import 'package:http/http.dart' as http;

class MatchesService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  static Future<List<Map<String, dynamic>>> fetchMatches() async {
    final response = await http.get(Uri.parse('$baseUrl/matches/'));
    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      return data.map<Map<String, dynamic>>((match) => {
        'match_id': match['match_id'],
        'date': match['date'],
        'location': match['location'],
        'start_time': match['start_time'],
        'referee_name': match['referee_name'],
        'end_time': match['end_time'],
      }).toList();
    } else {
      throw Exception('Failed to load matches');
    }
  }

  static Future<bool> addMatch(Map<String, dynamic> matchData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/matches/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(matchData),
    );
    return response.statusCode == 201;
  }

  static Future<bool> updateMatch(
    int matchId,
    Map<String, dynamic> updatedMatchData,
  ) async {
    final response = await http.put(
      Uri.parse('$baseUrl/matches/$matchId/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(updatedMatchData),
    );
    return response.statusCode == 200;
  }

  static Future<bool> deleteMatch(int matchId) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/matches/$matchId/'),
      headers: {'Content-Type': 'application/json'},
    );
    return response.statusCode == 204;
  }
}
