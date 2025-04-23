import 'dart:convert';
import 'package:http/http.dart' as http;

class TeamsService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  // Fetch all teams for a specific league
  // Fetch all teams for a specific league
  static Future<List<Team>> fetchTeams() async {
    final response = await http.get(Uri.parse('$baseUrl/teams/'));

    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);

      // Map the raw data to Team instances
      return data.map<Team>((teamData) {
        String teamName = teamData['name'];

        // Replace "Ã©" with "é" in team names
        teamName = teamName.replaceAll('Ã©', 'é');

        // Return the converted Team object
        return Team.fromMap({
          'name': teamName,
          'home_ground': teamData['home_ground'],
          'manager_name': teamData['manager_name'],
          'manager_dob': teamData['manager_dob'],
          'manager_seasons_headed': teamData['manager_seasons_headed'],
          'manager_date_joined': teamData['manager_date_joined'],
          'image': teamData['image'],
        });
      }).toList();
    } else {
      throw Exception('Failed to load teams');
    }
  }

  static Future<bool> addTeam(Team team) async {
    final response = await http.post(
      Uri.parse('$baseUrl/teams/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(team.toMap()),
    );
    return response.statusCode == 201;
  }

  static Future<bool> updateTeam(String oldName, Team updatedTeam) async {
    final encodedOldName = encodeForUrl(oldName);

    final response = await http.put(
      Uri.parse('$baseUrl/teams/$encodedOldName/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(updatedTeam.toMap()),
    );

    return response.statusCode == 200;
  }

  static Future<bool> deleteTeam(String teamName) async {
    final encodedName = encodeForUrl(teamName);

    final response = await http.delete(
      Uri.parse('$baseUrl/teams/$encodedName/'),
      headers: {'Content-Type': 'application/json'},
    );

    return response.statusCode == 204;
  }

  static String encodeForUrl(String input) {
    return Uri.encodeComponent(input);
  }
}
