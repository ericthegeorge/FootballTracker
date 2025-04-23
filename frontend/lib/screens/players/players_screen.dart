import 'package:flutter/material.dart';
import 'player_service.dart';
import '../../services/auth_service.dart';

enum PlayerScreenMode { view, select }

class PlayersScreen extends StatefulWidget {
  final PlayerScreenMode mode;

  const PlayersScreen({Key? key, this.mode = PlayerScreenMode.view})
    : super(key: key);

  @override
  State<PlayersScreen> createState() => _PlayersScreenState();
}

class _PlayersScreenState extends State<PlayersScreen> {
  List<String> allPlayers = [];
  List<String> filteredPlayers = [];
  Set<String> selectedPlayers = {};
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
      print('Admin status: $adminStatus');
      final players = await PlayerService.fetchPlayers();
      setState(() {
        isAdmin = adminStatus; // <- Save to state
        allPlayers = players;
        filteredPlayers = List.from(players);
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
                (player) => player.toLowerCase().contains(query.toLowerCase()),
              )
              .toList();
    });
  }

  void _addPlayer(String newPlayer) async {
    final success = await PlayerService.addPlayer(newPlayer);
    if (success) {
      setState(() {
        allPlayers.add(newPlayer);
        filteredPlayers.add(newPlayer);
      });
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to add player')));
    }
  }

  void _deletePlayer(String player) async {
    try {
      final success = await PlayerService.deletePlayer(player);
      if (success) {
        setState(() {
          allPlayers.remove(player);
          filteredPlayers.remove(player);
        });
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('$player has been deleted')));
      } else {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Failed to delete $player')));
      }
    } catch (e) {
      print('Failed to delete player: $e');
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  void _toggleSelection(String player) {
    setState(() {
      if (selectedPlayers.contains(player)) {
        selectedPlayers.remove(player);
      } else {
        selectedPlayers.add(player);
      }
    });
  }

  void _confirmDeletePlayer(String player) {
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Delete Player'),
            content: Text('Are you sure you want to delete $player?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text('Cancel'),
              ),
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  _deletePlayer(player);
                },
                child: Text('Delete'),
              ),
            ],
          ),
    );
  }

  void _showEditPlayerDialog(String oldName) {
    String newName = oldName;
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Edit Player'),
            content: TextField(
              onChanged: (value) => newName = value,
              controller: TextEditingController(text: oldName),
              decoration: InputDecoration(hintText: 'Enter new player name'),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text('Cancel'),
              ),
              TextButton(
                onPressed: () async {
                  Navigator.pop(context);
                  if (newName.trim().isNotEmpty && newName != oldName) {
                    final success = await PlayerService.updatePlayer(
                      oldName,
                      newName.trim(),
                    );
                    if (success) {
                      setState(() {
                        int index = allPlayers.indexOf(oldName);
                        allPlayers[index] = newName.trim();
                        _onSearchChanged(searchController.text);
                      });
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Failed to update $oldName')),
                      );
                    }
                  }
                },
                child: Text('Save'),
              ),
            ],
          ),
    );
  }

  void _showAddPlayerDialog() {
    String newPlayer = '';
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Add Player'),
            content: TextField(
              onChanged: (value) => newPlayer = value,
              decoration: InputDecoration(hintText: 'Enter player name'),
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  if (newPlayer.trim().isNotEmpty) {
                    _addPlayer(newPlayer.trim());
                  }
                },
                child: Text('Add'),
              ),
            ],
          ),
    );
  }

  void _onPlayerTapped(String player) {
    // if (isAdmin) return; // Admin behavior is already handled.

    // For non-admin users, show a dialog with options to view matches only (No further subdivision)
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Choose an option for $player'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  // Navigate to the matches screen (this should be a named route or widget)
                  Navigator.pushNamed(context, '/matches', arguments: player);
                },
                child: Text('View Matches'),
              ),
            ],
          ),
    );
  }

  Widget _buildPlayerItem(String player) {
    bool isSelectable = widget.mode == PlayerScreenMode.select;
    bool isSelected = selectedPlayers.contains(player);

    return ListTile(
      title: Text(player),
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
                    onPressed: () => _confirmDeletePlayer(player),
                  ),
                ],
              )
              : null, // Show nothing if not an admin
      onTap:
          isSelectable
              ? () => _onPlayerTapped(player)
              : () => _onPlayerTapped(player),
    );
  }

  @override
  Widget build(BuildContext context) {
    bool isSelectable = widget.mode == PlayerScreenMode.select;

    return Scaffold(
      appBar: AppBar(
        title: Text('Players'),
        actions: [
          if (isSelectable && selectedPlayers.isNotEmpty)
            TextButton(
              onPressed: () {
                // Do something with selectedPlayers
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Selected: ${selectedPlayers.join(', ')}'),
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
