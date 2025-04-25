import 'package:flutter/material.dart';
import 'package:frontend/screens/players/players_view_screen.dart';
import 'player_service.dart'; //Assuming this fetches player data from your API
import '../../services/auth_service.dart';

enum PlayerScreenMode { view, select }

class PlayersScreen extends StatefulWidget {
  final PlayerScreenMode mode;
  final String? team;

  const PlayersScreen({Key? key, this.mode = PlayerScreenMode.view, this.team})
    : super(key: key);

  @override
  State<PlayersScreen> createState() => _PlayersScreenState();
}

class _PlayersScreenState extends State<PlayersScreen> {
  List<Player> allPlayers = [];
  List<Player> filteredPlayers = [];
  Set<Player> selectedPlayers = {};
  TextEditingController searchController = TextEditingController();
  bool isAdmin = false;

  @override
  void initState() {
    super.initState();
    _loadPlayers();
  }

  Future<void> _loadPlayers() async {
    try {
      bool adminStatus = await AuthService.isAdmin();
      final results = await Future.wait([
        PlayerService.fetchPlayers(),
        PlayerService.getPlayerTeams(),
      ]);

      final playerMaps = results[0] as List<Map<String, dynamic>>;
      final playerTeamMap = results[1] as List<Map<String, String>>;
      final allFetchedPlayers = playerMaps.map((map) => Player.fromMap(map)).toList();

      final playersInThisTeam =
        playerTeamMap
          .where(
            (entry) =>
              entry['team_name'] != null &&
              entry['team_name'] == widget.team,
          )
          .map((entry) => entry['player_name'])
          .where(
            (playerName) => playerName != null,
          )
          .toSet();
      
      final filtered =
        allFetchedPlayers
          .where((player) => playersInThisTeam.contains(player.name))
          .toList();

      setState(() {
        isAdmin = adminStatus;
        allPlayers = filtered;
        filteredPlayers = filtered;
        });
      } catch (e) {
        print('Failed to load players: $e');
      }
  }

  void _onSearchChanged(String query) {
    setState(() {
      filteredPlayers =
          allPlayers
              .where(
                (player) => player.name.toLowerCase().contains(query.toLowerCase()),
              )
              .toList();
    });
  }

  void _addPlayer(Player newPlayer) async {
    final success = await PlayerService.addPlayer(
      newPlayer.toMap()
    );
    if (success) {
      setState(() {
        allPlayers.add(newPlayer);
        _onSearchChanged(searchController.text);
      });
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to add player')));
    }
  }

  void _deletePlayer(Player player) async {
    final success = await PlayerService.deletePlayer(
      player.name,
    );
    if (success) {
      setState(() {
        allPlayers.remove(player);
        filteredPlayers.remove(player);
      });
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('${player.name} has been deleted')));
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to delete ${player.name}')));
    }
  }

  void _toggleSelection(Player player) {
    setState(() {
      if (selectedPlayers.contains(player)) {
        selectedPlayers.remove(player);
      } else {
        selectedPlayers.add(player);
      }
    });
  }

  void _showEditPlayerDialog(Player player) {
    TextEditingController nameController = TextEditingController(
      text: player.name,
    );
    TextEditingController dobController = TextEditingController(
      text: player.dob.toIso8601String().split('T').first,
    );
    TextEditingController minutesPlayedController = TextEditingController(
      text: player.minutesPlayed.toString(),
    );
    TextEditingController matchesPlayedController = TextEditingController(
      text: player.matchesPlayed.toString(),
    );
    TextEditingController marketValueController = TextEditingController(
      text: player.marketValue.toString(),
    );
    TextEditingController preferredFootController = TextEditingController(
      text: player.preferredFoot,
    );
    TextEditingController heightController = TextEditingController(
      text: player.height.toString(),
    );
    TextEditingController yellowCardsController = TextEditingController(
      text: player.yellowCards.toString(),
    );
    TextEditingController redCardsController = TextEditingController(
      text: player.redCards.toString(),
    );
    TextEditingController playingTeamController = TextEditingController(
      text: player.playingTeam,
    );
    TextEditingController owningTeamController = TextEditingController(
      text: player.owningTeam,
    );

    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Edit Player: ${player.name}'),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextField(
                    controller: nameController,
                    decoration: InputDecoration(hintText: 'Player Name'),
                  ),
                  TextField(
                    controller: dobController,
                    decoration: InputDecoration(hintText: 'Player DOB (YYYY-MM-DD)'),
                    keyboardType:  TextInputType.datetime,
                  ),
                  TextField(
                    controller: minutesPlayedController,
                    decoration: InputDecoration(hintText: 'Minutes Played'),
                    keyboardType: TextInputType.number,
                  ),
                  TextField(
                    controller: matchesPlayedController,
                    decoration: InputDecoration(hintText: 'Matches Played'),
                    keyboardType: TextInputType.number,
                  ),
                  TextField(
                    controller: marketValueController,
                    decoration: InputDecoration(hintText: 'Market Value (millions)'),
                    keyboardType: TextInputType.numberWithOptions(decimal: true),
                  ),
                  TextField(
                    controller: preferredFootController,
                    decoration: InputDecoration(hintText: 'Preferred Foot (Left, Right or Two-Footed)'),
                  ),
                  TextField(
                    controller: heightController,
                    decoration: InputDecoration(hintText: 'Height (metres)'),
                    keyboardType: TextInputType.numberWithOptions(decimal: true),
                  ),
                  TextField(
                    controller: yellowCardsController,
                    decoration: InputDecoration(hintText: 'Yellow Cards'),
                    keyboardType: TextInputType.number,
                  ),
                  TextField(
                    controller: redCardsController,
                    decoration: InputDecoration(hintText: 'Red Cards'),
                    keyboardType: TextInputType.number,
                  ),
                  TextField(
                    controller: playingTeamController,
                    decoration: InputDecoration(hintText: 'Playing Team'),
                  ),
                  TextField(
                    controller: owningTeamController,
                    decoration: InputDecoration(hintText: 'Owning Team'),
                  ),
                ]
              )
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text('Cancel'),
              ),
              TextButton(
                onPressed: () async {
                  try {
                    Player updatedPlayer = Player(
                      name: nameController.text.trim(),
                      dob: DateTime.parse(dobController.text.trim()),
                      minutesPlayed: int.parse(minutesPlayedController.text.trim()),
                      matchesPlayed: int.parse(matchesPlayedController.text.trim()),
                      marketValue: double.parse(marketValueController.text.trim()),
                      preferredFoot: preferredFootController.text.trim(),
                      height: double.parse(heightController.text.trim()),
                      yellowCards: int.parse(yellowCardsController.text.trim()),
                      redCards: int.parse(redCardsController.text.trim()),
                      playingTeam: playingTeamController.text.trim(),
                      owningTeam: owningTeamController.text.trim(),
                    );
                    final success = await PlayerService.updatePlayer(
                      player.name,
                      updatedPlayer.toMap(),
                    );
                    if (success) {
                      setState(() {
                        int index = allPlayers.indexOf(player);
                        allPlayers[index] = updatedPlayer;
                        _onSearchChanged(
                          searchController.text,
                        );
                      });
                      Navigator.pop(context);
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Failed to update player')),
                      );
                    }
                  } catch (e) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('Invalid input. Please check all fields.'),
                      )
                    );
                  }
                },
                child: Text('Save'),
              ),
            ],
          ),
    );
  }

  void _showAddPlayerDialog() {
    TextEditingController nameController = TextEditingController();
    TextEditingController dobController = TextEditingController();
    TextEditingController minutesPlayedController = TextEditingController();
    TextEditingController matchesPlayedController = TextEditingController();
    TextEditingController marketValueController = TextEditingController();
    TextEditingController preferredFootController = TextEditingController();
    TextEditingController heightController = TextEditingController();
    TextEditingController yellowCardsController = TextEditingController();
    TextEditingController redCardsController = TextEditingController();
    TextEditingController playingTeamController = TextEditingController();
    TextEditingController owningTeamController = TextEditingController();

    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Add Player'),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextField(
                    controller: nameController,
                    decoration: InputDecoration(hintText: 'Player Name'),
                  ),
                  TextField(
                    controller: dobController,
                    decoration: InputDecoration(hintText: 'Player DOB (YYYY-MM-DD)'),
                    keyboardType:  TextInputType.datetime,
                  ),
                  TextField(
                    controller: minutesPlayedController,
                    decoration: InputDecoration(hintText: 'Minutes Played'),
                    keyboardType: TextInputType.number,
                  ),
                  TextField(
                    controller: matchesPlayedController,
                    decoration: InputDecoration(hintText: 'Matches Played'),
                    keyboardType: TextInputType.number,
                  ),
                  TextField(
                    controller: marketValueController,
                    decoration: InputDecoration(hintText: 'Market Value (millions)'),
                    keyboardType: TextInputType.numberWithOptions(decimal: true),
                  ),
                  TextField(
                    controller: preferredFootController,
                    decoration: InputDecoration(hintText: 'Preferred Foot (Left, Right or Two-Footed)'),
                  ),
                  TextField(
                    controller: heightController,
                    decoration: InputDecoration(hintText: 'Height (metres)'),
                    keyboardType: TextInputType.numberWithOptions(decimal: true),
                  ),
                  TextField(
                    controller: yellowCardsController,
                    decoration: InputDecoration(hintText: 'Yellow Cards'),
                    keyboardType: TextInputType.number,
                  ),
                  TextField(
                    controller: redCardsController,
                    decoration: InputDecoration(hintText: 'Red Cards'),
                    keyboardType: TextInputType.number,
                  ),
                  TextField(
                    controller: playingTeamController,
                    decoration: InputDecoration(hintText: 'Playing Team'),
                  ),
                  TextField(
                    controller: owningTeamController,
                    decoration: InputDecoration(hintText: 'Owning Team'),
                  ),
                ]
              )
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text('Cancel'),
              ),
              TextButton(
                onPressed: () {
                  String name = nameController.text.trim();
                  String dobText = dobController.text.trim();
                  String minutesPlayedText = minutesPlayedController.text.trim();
                  String matchesPlayedText = matchesPlayedController.text.trim();
                  String marketValueText = marketValueController.text.trim();
                  String preferredFoot = preferredFootController.text.trim();
                  String heightText = heightController.text.trim();
                  String yellowCardsText = yellowCardsController.text.trim();
                  String redCardsText = redCardsController.text.trim();
                  String playingTeam = playingTeamController.text.trim();
                  String owningTeam = owningTeamController.text.trim();

                  if (name.isNotEmpty &&
                      dobText.isNotEmpty &&
                      minutesPlayedText.isNotEmpty &&
                      matchesPlayedText.isNotEmpty &&
                      marketValueText.isNotEmpty &&
                      preferredFoot.isNotEmpty &&
                      heightText.isNotEmpty &&
                      yellowCardsText.isNotEmpty &&
                      redCardsText.isNotEmpty &&
                      playingTeam.isNotEmpty &&
                      owningTeam.isNotEmpty) {
                    try {
                      Player newPlayer = Player(
                        name: name,
                        dob: DateTime.parse(dobText),
                        minutesPlayed: int.parse(minutesPlayedText),
                        matchesPlayed: int.parse(matchesPlayedText),
                        marketValue: double.parse(marketValueText),
                        preferredFoot: preferredFoot,
                        height: double.parse(heightText),
                        yellowCards: int.parse(yellowCardsText),
                        redCards: int.parse(redCardsText),
                        playingTeam: playingTeam,
                        owningTeam: owningTeam,
                      );
                      _addPlayer(newPlayer);
                      Navigator.pop(context);
                    } catch (e) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Invalid date or number format.'),
                        ),
                      );
                    }
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('All fields must be filled.')),
                    );
                  }
                },
                child: Text('Add'),
              ),
            ],
          ),
    );
  }

  Widget _buildPlayerItem(Player player) {
    bool isSelectable = widget.mode == PlayerScreenMode.select;
    bool isSelected = selectedPlayers.contains(player);

    return ListTile(
      title: Text(player.name, overflow: TextOverflow.ellipsis),
      subtitle: Text(
        'Date of Birth: ${player.dob}\nMinutes Played: ${player.minutesPlayed}\nMatches Played: ${player.matchesPlayed}\n Market Value (in millions): ${player.marketValue}\nPreferred Foot: ${player.preferredFoot}\nHeight (in metres): ${player.height}\nYellow Cards: ${player.yellowCards}\nRed Cards: ${player.redCards}\nPlaying Team: ${player.playingTeam}\nOwning Team: ${player.owningTeam}',
      ),
      trailing:
          isSelectable
              ? Checkbox(
                value: isSelected,
                onChanged: (_) => _toggleSelection(player),
              )
              : isAdmin
              ? Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  IconButton(
                    icon: Icon(Icons.edit),
                    onPressed: () => _showEditPlayerDialog(player),
                  ),
                  IconButton(
                    icon: Icon(Icons.delete),
                    onPressed: () => _deletePlayer(player),
                  ),
                ],
              )
              : null, // Show nothing if not an admin
      onTap: isSelectable ? () => _toggleSelection(player) : null,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Players'),
        actions: [
          if (widget.mode == PlayerScreenMode.select && selectedPlayers.isNotEmpty)
            TextButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      'Selected: ${selectedPlayers.map((e) => e.name).join(', ')}',
                    ),
                  ),
                );
              },
              child: Text('Confirm', style: TextStyle(color: Colors.white)),
            ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: TextField(
              controller: searchController,
              onChanged: _onSearchChanged,
              decoration: InputDecoration(
                hintText: 'Search players...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filteredPlayers.length,
              itemBuilder:
                  (_, index) => _buildPlayerItem(filteredPlayers[index]),
            ),
          ),
        ],
      ),
      floatingActionButton:
          isAdmin
              ? FloatingActionButton(
                onPressed: _showAddPlayerDialog,
                child: Icon(Icons.add),
                tooltip: 'Add Player',
              )
              : null,
    );
  }
}

class Player {
  final String name;
  final DateTime dob;
  final int minutesPlayed;
  final int matchesPlayed;
  final double marketValue;
  final String preferredFoot;
  final double height;
  final int yellowCards;
  final int redCards;
  final String playingTeam;
  final String owningTeam;

  Player({
  required this.name ,
  required this.dob ,
  required this.minutesPlayed ,
  required this.matchesPlayed ,
  required this.marketValue ,
  required this.preferredFoot ,
  required this.height ,
  required this.yellowCards ,
  required this.redCards ,
  required this.playingTeam ,
  required this.owningTeam ,
  });

  //Factory constructor, creating player from map
  factory Player.fromMap(Map<String, dynamic> map) {
    return Player(
      name: map['name'],
      dob: DateTime.parse(map['dob']),
      minutesPlayed: int.parse(map['minutes_played']),
      matchesPlayed: int.parse(map['matches_played']),
      marketValue: double.parse(map['market_value']),
      preferredFoot: map['preferred_foot'],
      height: double.parse(map['height']),
      yellowCards: int.parse(map['yellow_cards']),
      redCards: int.parse(map['red_cards']),
      playingTeam: map['playing_team_id'],
      owningTeam: map['owning_team_id'],
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'dob': dob.toIso8601String(),
      'minutes_played': minutesPlayed,
      'matches_played': matchesPlayed,
      'market_value': marketValue,
      'preferred_foot': preferredFoot,
      'height': height,
      'yellow_cards': yellowCards,
      'red_cards': redCards,
      'playing_team_id': playingTeam,
      'owning_team_id': owningTeam,
    };
  }
}