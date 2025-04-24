import 'package:flutter/material.dart';
import 'package:frontend/routes.dart';
import 'league_service.dart';
import '../../services/auth_service.dart';

enum LeagueScreenMode { view, select }

class LeaguesScreen extends StatefulWidget {
  final LeagueScreenMode mode;

  const LeaguesScreen({Key? key, this.mode = LeagueScreenMode.view})
    : super(key: key);

  @override
  State<LeaguesScreen> createState() => _LeaguesScreenState();
}

class _LeaguesScreenState extends State<LeaguesScreen> {
  List<String> allLeagues = [];
  List<String> filteredLeagues = [];
  Set<String> selectedLeagues = {};
  TextEditingController searchController = TextEditingController();
  bool isAdmin = false;

  @override
  void initState() {
    super.initState();
    _loadLeagues();
  }

  Future<void> _loadLeagues() async {
    try {
      bool adminStatus = await AuthService.isAdmin();
      print('Admin status: $adminStatus');
      final leagues = await LeagueService.fetchLeagues();
      setState(() {
        isAdmin = adminStatus; // <- Save to state
        allLeagues = leagues;
        filteredLeagues = List.from(leagues);
      });
    } catch (e) {
      print('Failed to load leagues: $e');
    }
  }

  void _onSearchChanged(String query) {
    setState(() {
      filteredLeagues =
          allLeagues
              .where(
                (league) => league.toLowerCase().contains(query.toLowerCase()),
              )
              .toList();
    });
  }

  void _addLeague(String newLeague) async {
    final success = await LeagueService.addLeague(newLeague);
    if (success) {
      setState(() {
        allLeagues.add(newLeague);
        filteredLeagues.add(newLeague);
      });
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to add league')));
    }
  }

  void _deleteLeague(String league) async {
    try {
      final success = await LeagueService.deleteLeague(league);
      if (success) {
        setState(() {
          allLeagues.remove(league);
          filteredLeagues.remove(league);
        });
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('$league has been deleted')));
      } else {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Failed to delete $league')));
      }
    } catch (e) {
      print('Failed to delete league: $e');
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  void _toggleSelection(String league) {
    setState(() {
      if (selectedLeagues.contains(league)) {
        selectedLeagues.remove(league);
      } else {
        selectedLeagues.add(league);
      }
    });
  }

  void _confirmDeleteLeague(String league) {
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Delete League'),
            content: Text('Are you sure you want to delete $league?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text('Cancel'),
              ),
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  _deleteLeague(league);
                },
                child: Text('Delete'),
              ),
            ],
          ),
    );
  }

  void _showEditLeagueDialog(String oldName) {
    String newName = oldName;
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Edit League'),
            content: TextField(
              onChanged: (value) => newName = value,
              controller: TextEditingController(text: oldName),
              decoration: InputDecoration(hintText: 'Enter new league name'),
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
                    final success = await LeagueService.updateLeague(
                      oldName,
                      newName.trim(),
                    );
                    if (success) {
                      setState(() {
                        int index = allLeagues.indexOf(oldName);
                        allLeagues[index] = newName.trim();
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

  void _showAddLeagueDialog() {
    String newLeague = '';
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Add League'),
            content: TextField(
              onChanged: (value) => newLeague = value,
              decoration: InputDecoration(hintText: 'Enter league name'),
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  if (newLeague.trim().isNotEmpty) {
                    _addLeague(newLeague.trim());
                  }
                },
                child: Text('Add'),
              ),
            ],
          ),
    );
  }

  void _onLeagueTapped(String league) {
    // if (isAdmin) return; // Admin behavior is already handled.

    // For non-admin users, show a dialog with options to view teams or matches
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Choose an option for $league'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  // Navigate to the teams screen (this should be a named route or widget)
                  Navigator.pushNamed(context, Routes.teams, arguments: league);
                },
                child: Text('View Teams'),
              ),
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  // Navigate to the matches screen (this should be a named route or widget)
                  Navigator.pushNamed(
                    context,
                    Routes.matches,
                    arguments: league,
                  );
                },
                child: Text('View Matches'),
              ),
            ],
          ),
    );
  }

  Widget _buildLeagueItem(String league) {
    bool isSelectable = widget.mode == LeagueScreenMode.select;
    bool isSelected = selectedLeagues.contains(league);

    return ListTile(
      title: Text(league),
      trailing:
          isSelectable
              ? Checkbox(
                value: isSelected,
                onChanged: (_) => _toggleSelection(league),
              )
              : isAdmin
              ? Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  IconButton(
                    icon: Icon(Icons.edit),
                    onPressed: () => _showEditLeagueDialog(league),
                  ),
                  IconButton(
                    icon: Icon(Icons.delete),
                    onPressed: () => _confirmDeleteLeague(league),
                  ),
                ],
              )
              : null, // Show nothing if not an admin
      onTap:
          isSelectable
              ? () => _onLeagueTapped(league)
              : () => _onLeagueTapped(league),
    );
  }

  @override
  Widget build(BuildContext context) {
    bool isSelectable = widget.mode == LeagueScreenMode.select;

    return Scaffold(
      appBar: AppBar(
        title: Text('Leagues'),
        actions: [
          if (isSelectable && selectedLeagues.isNotEmpty)
            TextButton(
              onPressed: () {
                // Do something with selectedLeagues
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Selected: ${selectedLeagues.join(', ')}'),
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
                hintText: 'Search leagues...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filteredLeagues.length,
              itemBuilder:
                  (_, index) => _buildLeagueItem(filteredLeagues[index]),
            ),
          ),
        ],
      ),
      floatingActionButton:
          isAdmin
              ? FloatingActionButton(
                onPressed: _showAddLeagueDialog,
                child: Icon(Icons.add),
                tooltip: 'Add League',
              )
              : null,
    );
  }
}
