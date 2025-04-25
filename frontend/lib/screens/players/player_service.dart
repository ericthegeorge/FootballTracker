import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

class PlayerService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';
  final DateFormat formatter = DateFormat('yyyy-MM-dd');

  static Future<List<Map<String, dynamic>>> fetchPlayers() async {
    final response = await http.get(Uri.parse('$baseUrl/players/'));
    
    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);

      //Special character processing
      return data.map<Map<String, dynamic>>((player) {
        String playerName = player['name'];

        playerName = playerName.replaceAll('Ã©', 'é');
        playerName = playerName.replaceAll('Ã', 'í');
        playerName = playerName.replaceAll('Ã¡', 'á');
        playerName = playerName.replaceAll('í', 'Í');
        playerName = playerName.replaceAll('í±', 'ñ');

        print('Decoded Player Name: $playerName\n'); //Debugging

        return {
          'player_id': player['player_id'],
          'name': playerName,
          'dob': player['dob'],
          'minutes_played': player['minutes_played'],
          'matches_played': player['matches_played'],
          'market_value': player['market_value'],
          'preferred_foot': player['preferred_foot'],
          'height': player['height'],
          'yellow_cards': player['yellow_cards'],
          'red_cards': player['red_cards'],
          'playing_team_id': player['playing_team_id'],
          'owning_team_id': player['owning_team_id'],
        };
      }).toList();
      
    } else {
      throw Exception('Failed to load players');
    }
  }

  static String encodeForUrl(String input) {
    return Uri.encodeComponent(input);
  }

  static Future<bool> addPlayer(Map<String, dynamic> playerData) async {
    // Format date fields before sending the request
    playerData['dob'] = DateFormat(
      'yyyy-MM-dd',
    ).format(DateTime.parse(playerData['manager_dob']));

    final response = await http.post(
      Uri.parse('$baseUrl/players/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(playerData),
    );
    return response.statusCode == 201;
  }

  static Future<bool> updatePlayer(
    String oldName, 
    Map<String, dynamic> updatedPlayerData,
    ) async {
      // Format date fields before sending the request
      updatedPlayerData['dob'] = DateFormat(
        'yyyy-MM-dd',
      ).format(DateTime.parse(updatedPlayerData['manager_dob']));

      final encodedOldName = encodeForUrl(oldName);

      final response = await http.put(
        Uri.parse('$baseUrl/players/$encodedOldName'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'name': updatedPlayerData}),
      );

      return response.statusCode == 200;
    }

    static Future<bool> deletePlayer(String playerName) async {
    final encodedName = encodeForUrl(playerName);

    final response = await http.delete(
      Uri.parse('$baseUrl/players/$encodedName'),
      headers: {'Content-Type': 'application/json'},
    );

    return response.statusCode == 204;
  }

  static Future<List<Map<String, String>>> getPlayerTeams() async {
    final response = await http.get(
      Uri.parse('$baseUrl/player-works-with-team'),
      headers: {'Content-Type': 'application/json'},
    );
    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      return data.map<Map<String, String>>((item) {
        return {'player_name': item['player_id'], 'team_name': item['team_id']};
      }).toList();
    } else {
      throw Exception('Failed to load team-league pairs');
    }
  }
}