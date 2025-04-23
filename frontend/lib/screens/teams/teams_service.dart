import 'dart:convert';
import 'package:http/http.dart' as http;

class TeamsService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  // Fetch all teams for a specific league
  // Fetch all teams for a specific league
  static Future<List<Map<String, dynamic>>> fetchTeams() async {
    final response = await http.get(Uri.parse('$baseUrl/teams/'));

    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);

      // Processing data to replace the characters in team names
      return data.map<Map<String, dynamic>>((team) {
        String teamName = team['name'];

        // Replace "Ã©" with "é"
        teamName = teamName.replaceAll('Ã©', 'é');

        print(
          'Decoded Team Name: $teamName',
        ); // Print the team name for debugging

        // Create a new map with the team data, replacing the team name as needed
        return {
          'name': teamName,
          'home_ground': team['home_ground'],
          'manager_name': team['manager_name'],
          'manager_dob': team['manager_dob'],
          'manager_seasons_headed': team['manager_seasons_headed'],
          'manager_date_joined': team['manager_date_joined'],
          'image': team['image'],
        };
      }).toList();
    } else {
      throw Exception('Failed to load teams');
    }
  }

  static String encodeForUrl(String input) {
    return Uri.encodeComponent(input);
  }

  static Future<bool> addTeam(Map<String, dynamic> teamData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/teams/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(teamData),
    );
    return response.statusCode == 201;
  }

  static Future<bool> updateTeam(
    String oldName,
    Map<String, dynamic> updatedTeamData,
  ) async {
    final encodedOldName = encodeForUrl(oldName);

    final response = await http.put(
      Uri.parse('$baseUrl/teams/$encodedOldName/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(updatedTeamData),
    );

    return response.statusCode == 200;
  }

  static Future<bool> deleteTeam(String teamName) async {
    final encodedName = encodeForUrl(teamName);

    final response = await http.delete(
      Uri.parse('$baseUrl/teams/$encodedName/'),
      headers: {'Content-Type': 'application/json'},
    );

    return response.statusCode == 204; // No content on successful delete
  }
}
