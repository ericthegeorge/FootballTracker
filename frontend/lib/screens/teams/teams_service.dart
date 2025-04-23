import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

class TeamsService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  // Fetch all teams for a specific league
  // Fetch all teams for a specific league
  final DateFormat formatter = DateFormat('yyyy-MM-dd');

  static Future<List<Map<String, dynamic>>> fetchTeams() async {
    final response = await http.get(Uri.parse('$baseUrl/teams/'));

    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);

      // Processing data to replace the characters in team names
      return data.map<Map<String, dynamic>>((team) {
        String teamName = team['name'];
        String manager_name = team['manager_name'];
        String home_ground = team['home_ground'];

        // Replace "Ã©" with "é"
        teamName = teamName.replaceAll('Ã©', 'é');
        teamName = teamName.replaceAll('Ã', 'í');
        teamName = teamName.replaceAll('Ã¡', 'á');
        teamName = teamName.replaceAll('í', 'Í');
        teamName = teamName.replaceAll('í±', 'ñ');

        // teamName = teamName.replaceAll('')

        manager_name = manager_name.replaceAll('Ã©', 'é');
        manager_name = manager_name.replaceAll('Ã¡', 'á');
        manager_name = manager_name.replaceAll('Ã', 'í');
        manager_name = manager_name.replaceAll('í', 'Í');
        manager_name = manager_name.replaceAll('í±', 'ñ');

        home_ground = home_ground.replaceAll('Ã©', 'é');
        home_ground = home_ground.replaceAll('Ã¡', 'á');
        home_ground = home_ground.replaceAll('Ã', 'í');
        home_ground = home_ground.replaceAll('í', 'Í');
        home_ground = home_ground.replaceAll('í±', 'ñ');

        print(
          'Decoded Team Name: $teamName\n',
        ); // Print the team name for debugging

        print(team['image']);
        // Create a new map with the team data, replacing the team name as needed
        return {
          'name': teamName,
          'home_ground': home_ground,
          'manager_name': manager_name,
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
    // Format date fields before sending the request
    teamData['manager_dob'] = DateFormat(
      'yyyy-MM-dd',
    ).format(DateTime.parse(teamData['manager_dob']));
    teamData['manager_date_joined'] = DateFormat(
      'yyyy-MM-dd',
    ).format(DateTime.parse(teamData['manager_date_joined']));

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
    // Format date fields before sending the request
    updatedTeamData['manager_dob'] = DateFormat(
      'yyyy-MM-dd',
    ).format(DateTime.parse(updatedTeamData['manager_dob']));
    updatedTeamData['manager_date_joined'] = DateFormat(
      'yyyy-MM-dd',
    ).format(DateTime.parse(updatedTeamData['manager_date_joined']));

    print(updatedTeamData['manager_dob']);
    print(updatedTeamData['manager_date_joined']);

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
