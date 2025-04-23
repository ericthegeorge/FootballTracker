import 'package:flutter/material.dart';
import 'player_service.dart';
import '../../services/auth_service.dart';

class PlayersScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Player Screen')),
      body: Center(child: Text('This is the Player screen')),
    );
  }
}
