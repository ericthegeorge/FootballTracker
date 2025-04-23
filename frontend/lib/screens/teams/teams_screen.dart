import 'package:flutter/material.dart';
import 'teams_service.dart'; // Assuming this fetches team data from your API
import '../../services/auth_service.dart';

enum TeamScreenMode { view, select }

class TeamsScreen extends StatefulWidget {
  final TeamScreenMode mode;

  const TeamsScreen({Key? key, this.mode = TeamScreenMode.view})
    : super(key: key);

  @override
  State<TeamsScreen> createState() => _TeamsScreenState();
}

class _TeamsScreenState extends State<TeamsScreen> {
  List<Team> allTeams = [];
  List<Team> filteredTeams = [];
  Set<Team> selectedTeams = {};
  TextEditingController searchController = TextEditingController();
  bool isAdmin = false;

  @override
  void initState() {
    super.initState();
    _loadTeams();
  }

  Future<void> _loadTeams() async {
    try {
      bool adminStatus = await AuthService.isAdmin();
      final teams =
          await TeamsService.fetchTeams(); // Assume this fetches a list of Team objects
      setState(() {
        isAdmin = adminStatus;
        allTeams = teams.map((map) => Team.fromMap(map)).toList();
        filteredTeams = allTeams;
      });
    } catch (e) {
      print('Failed to load teams: $e');
    }
  }

  void _onSearchChanged(String query) {
    setState(() {
      filteredTeams =
          allTeams
              .where(
                (team) => team.name.toLowerCase().contains(query.toLowerCase()),
              )
              .toList();
    });
  }

  void _addTeam(Team newTeam) async {
    final success = await TeamsService.addTeam(
      newTeam.toMap(),
    ); // Assume you have addTeam method
    if (success) {
      setState(() {
        allTeams.add(newTeam);
        filteredTeams.add(newTeam);
      });
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to add team')));
    }
  }

  void _deleteTeam(Team team) async {
    final success = await TeamsService.deleteTeam(
      team.name,
    ); // Delete by team name
    if (success) {
      setState(() {
        allTeams.remove(team);
        filteredTeams.remove(team);
      });
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('${team.name} has been deleted')));
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to delete ${team.name}')));
    }
  }

  void _toggleSelection(Team team) {
    setState(() {
      if (selectedTeams.contains(team)) {
        selectedTeams.remove(team);
      } else {
        selectedTeams.add(team);
      }
    });
  }

  void _showEditTeamDialog(Team team) {
    TextEditingController nameController = TextEditingController(
      text: team.name,
    );
    TextEditingController homeGroundController = TextEditingController(
      text: team.homeGround,
    );
    TextEditingController managerNameController = TextEditingController(
      text: team.managerName,
    );

    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Edit Team: ${team.name}'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: nameController,
                  decoration: InputDecoration(hintText: 'Team Name'),
                ),
                TextField(
                  controller: homeGroundController,
                  decoration: InputDecoration(hintText: 'Home Ground'),
                ),
                TextField(
                  controller: managerNameController,
                  decoration: InputDecoration(hintText: 'Manager Name'),
                ),
                // Add more fields as needed for managerDob, managerSeasonsHeaded, etc.
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text('Cancel'),
              ),
              TextButton(
                onPressed: () async {
                  String newName = nameController.text.trim();
                  String newHomeGround = homeGroundController.text.trim();
                  String newManagerName = managerNameController.text.trim();
                  // You can collect and validate other fields as needed
                  if (newName.isNotEmpty && newHomeGround.isNotEmpty) {
                    Team updatedTeam = Team(
                      name: newName,
                      homeGround: newHomeGround,
                      managerDob: team.managerDob, // Keep existing dob
                      managerName: newManagerName,
                      managerSeasonsHeaded: team.managerSeasonsHeaded,
                      managerDateJoined: team.managerDateJoined,
                      image: team.image,
                    );
                    final success = await TeamsService.updateTeam(
                      team.name,
                      updatedTeam.toMap(),
                    );
                    if (success) {
                      setState(() {
                        int index = allTeams.indexOf(team);
                        allTeams[index] = updatedTeam;
                        filteredTeams[index] = updatedTeam;
                      });
                      Navigator.pop(context);
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Failed to update team')),
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

  Widget _buildTeamItem(Team team) {
    bool isSelectable = widget.mode == TeamScreenMode.select;
    bool isSelected = selectedTeams.contains(team);

    return ListTile(
      title: Text(team.name),
      subtitle: Text('${team.homeGround}\nManager: ${team.managerName}'),
      trailing:
          isSelectable
              ? Checkbox(
                value: isSelected,
                onChanged: (_) => _toggleSelection(team),
              )
              : isAdmin
              ? Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  IconButton(
                    icon: Icon(Icons.edit),
                    onPressed: () => _showEditTeamDialog(team),
                  ),
                  IconButton(
                    icon: Icon(Icons.delete),
                    onPressed: () => _deleteTeam(team),
                  ),
                ],
              )
              : null,
      onTap: isSelectable ? () => _toggleSelection(team) : null,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Teams'),
        actions: [
          if (widget.mode == TeamScreenMode.select && selectedTeams.isNotEmpty)
            TextButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      'Selected: ${selectedTeams.map((e) => e.name).join(', ')}',
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
                hintText: 'Search teams...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filteredTeams.length,
              itemBuilder: (_, index) => _buildTeamItem(filteredTeams[index]),
            ),
          ),
        ],
      ),
      floatingActionButton:
          isAdmin
              ? FloatingActionButton(
                onPressed: () {
                  _addTeam(
                    Team(
                      name: '',
                      homeGround: '',
                      managerDob: DateTime.now(),
                      managerName: '',
                      managerSeasonsHeaded: 0,
                      managerDateJoined: DateTime.now(),
                      image: '',
                    ),
                  );
                },
                child: Icon(Icons.add),
                tooltip: 'Add Team',
              )
              : null,
    );
  }
}

class Team {
  final String name;
  final String homeGround;
  final DateTime managerDob;
  final String managerName;
  final int managerSeasonsHeaded;
  final DateTime managerDateJoined;
  final String image;

  Team({
    required this.name,
    required this.homeGround,
    required this.managerDob,
    required this.managerName,
    required this.managerSeasonsHeaded,
    required this.managerDateJoined,
    required this.image,
  });

  // Factory constructor to create a Team from a Map
  factory Team.fromMap(Map<String, dynamic> map) {
    return Team(
      name: map['name'],
      homeGround: map['home_ground'],
      managerDob: DateTime.parse(map['manager_dob']),
      managerName: map['manager_name'],
      managerSeasonsHeaded: map['manager_seasons_headed'],
      managerDateJoined: DateTime.parse(map['manager_date_joined']),
      image: map['image'],
    );
  }

  // Convert a Team to a Map for API calls
  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'home_ground': homeGround,
      'manager_dob': managerDob.toIso8601String(),
      'manager_name': managerName,
      'manager_seasons_headed': managerSeasonsHeaded,
      'manager_date_joined': managerDateJoined.toIso8601String(),
      'image': image,
    };
  }
}
