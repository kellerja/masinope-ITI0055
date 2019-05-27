:- dynamic(player/2).
:- dynamic(player/1).

size(4, 4).

player(1, 1).
player(alive).
arrows(1).

/* Build board */

:- dynamic(board/2).
:- dynamic(breezy/2).
:- dynamic(pit/2).
:- dynamic(wumpus/2).
:- dynamic(smelly/2).
:- dynamic(treasure/2).

make_board(1, 1) :- 
    assertz(board(1, 1)).
make_board(1, Y) :-
    assertz(board(1, Y)),
    New_Y is Y - 1,
    size(X, _),
    make_board(X, New_Y).
make_board(X, Y) :-
    assertz(board(X, Y)),
    New_X is X - 1,
    make_board(New_X, Y).

add_breeze(X, Y) :-
    breezy(X, Y), !.
add_breeze(X, Y) :-
    size(Max_X, Max_Y),
    X =< Max_X, Y =< Max_Y,
    assertz(breezy(X, Y)).
add_breeze(_, _).

add_pit(X, Y) :-
    pit(X, Y), !.
add_pit(X, Y) :-
    size(Max_X, Max_Y),
    X =< Max_X, Y =< Max_Y,
    assertz(pit(X, Y)),
    Top_Y is Y + 1,
    add_breeze(X, Top_Y),
    Right_X is X + 1,
    add_breeze(Right_X, Y),
    Bottom_Y is Y - 1,
    add_breeze(X, Bottom_Y),
    Left_X is X - 1,
    add_breeze(Left_X, Y), !.

add_smelly(X, Y) :-
    smelly(X, Y), !.
add_smelly(X, Y) :-
    size(Max_X, Max_Y),
    X =< Max_X, Y =< Max_Y,
    assertz(smelly(X, Y)), !.
add_smelly(_, _).

add_wumpus(X, Y) :-
    wumpus(X, Y), !.
add_wumpus(X, Y) :-
    size(Max_X, Max_Y),
    X =< Max_X, Y =< Max_Y,
    assertz(wumpus(X, Y)),
    Top_Y is Y + 1,
    add_smelly(X, Top_Y),
    Right_X is X + 1,
    add_smelly(Right_X, Y),
    Bottom_Y is Y - 1,
    add_smelly(X, Bottom_Y),
    Left_X is X - 1,
    add_smelly(Left_X, Y), !.

add_treasure(X, Y) :-
    treasure(X, Y), !.
add_treasure(X, Y) :-
    size(Max_X, Max_Y),
    X =< Max_X, Y =< Max_Y,
    assertz(treasure(X, Y)), !.

make_board :-
    size(X, Y),
    make_board(X, Y),
    add_pit(3, 1),
    add_pit(3, 3),
    add_pit(4, 4),
    add_wumpus(3, 4),
    add_treasure(2, 3), !.

print_cell(X, Y) :-
    (pit(X, Y), write('O');
    wumpus(X, Y), write('M');
    player(X, Y), write('P');
    smelly(X, Y), breezy(X, Y), treasure(X, Y), write('*');
    smelly(X, Y), breezy(X, Y), write('=');
    smelly(X, Y), treasure(X, Y), write('/');
    treasure(X, Y), breezy(X, Y), write('\\');
    smelly(X, Y), write('-');
    breezy(X, Y), write('~');
    treasure(X, Y), write('T');
    write(' ')), !.

print_board(X, 1, X) :- nl, !.
print_board(X_Max, Y, X_Max) :-
    board(1, Y),
    nl,
    New_Y is Y - 1,
    print_board(1, New_Y, X_Max), !.
print_board(X, Y, X_Max) :-
    board(X, Y),
    print_cell(X, Y), 
    New_X is X + 1,
    print_board(New_X, Y, X_Max), !.

print_board :-
    size(Max_X, Max_Y),
    Max_X_Inc is Max_X + 1,
    print_board(1, Max_Y, Max_X_Inc).

/* Logic as agent */
:- dynamic(player_board/2).
:- dynamic(player_smelly/2).
:- dynamic(player_breezy/2).
:- dynamic(player_safe/2).
:- dynamic(player_pit/2).
:- dynamic(player_wumpus/2).
:- dynamic(player_possible_pit/2).
:- dynamic(player_possible_wumpus/2).

mark_possible_wumpus_left(X, Y) :-
    X_left is X - 1,
    player_board(X_left, Y).
mark_possible_wumpus_left(X, Y) :-
    X_left is X - 1,
    board(X_left, Y),
    (player_possible_wumpus(X_left, Y); assert(player_possible_wumpus(X_left, Y))).
mark_possible_wumpus_left(_, _).

mark_possible_wumpus_right(X, Y) :-
    X_right is X + 1,
    player_board(X_right, Y).
mark_possible_wumpus_right(X, Y) :-
    X_right is X + 1,
    board(X_right, Y),
    (player_possible_wumpus(X_right, Y); assert(player_possible_wumpus(X_right, Y))).
mark_possible_wumpus_right(_, _).

mark_possible_wumpus_top(X, Y) :-
    Y_top is Y + 1,
    player_board(X, Y_top).
mark_possible_wumpus_top(X, Y) :-
    Y_top is Y + 1,
    board(X, Y_top),
    (player_possible_wumpus(X, Y_top); assert(player_possible_wumpus(X, Y_top))).
mark_possible_wumpus_top(_, _).

mark_possible_wumpus_bottom(X, Y) :-
    Y_bottom is Y - 1,
    player_board(X, Y_bottom).
mark_possible_wumpus_bottom(X, Y) :-
    Y_bottom is Y - 1,
    board(X, Y_bottom),
    (player_possible_wumpus(X, Y_bottom); assert(player_possible_wumpus(X, Y_bottom))).
mark_possible_wumpus_bottom(_, _).

mark_possible_wumpus(X, Y) :-
    mark_possible_wumpus_top(X, Y),
    mark_possible_wumpus_left(X, Y),
    mark_possible_wumpus_bottom(X, Y),
    mark_possible_wumpus_right(X, Y), !.

mark_possible_pit_left(X, Y) :-
    X_left is X - 1,
    player_board(X_left, Y).
mark_possible_pit_left(X, Y) :-
    X_left is X - 1,
    board(X_left, Y),
    (player_possible_pit(X_left, Y); assert(player_possible_pit(X_left, Y))).
mark_possible_pit_left(_, _).

mark_possible_pit_right(X, Y) :-
    X_right is X + 1,
    player_board(X_right, Y).
mark_possible_pit_right(X, Y) :-
    X_right is X + 1,
    board(X_right, Y),
    (player_possible_pit(X_right, Y); assert(player_possible_pit(X_right, Y))).
mark_possible_pit_right(_, _).

mark_possible_pit_top(X, Y) :-
    Y_top is Y + 1,
    player_board(X, Y_top).
mark_possible_pit_top(X, Y) :-
    Y_top is Y + 1,
    board(X, Y_top),
    (player_possible_pit(X, Y_top); assert(player_possible_pit(X, Y_top))).
mark_possible_pit_top(_, _).

mark_possible_pit_bottom(X, Y) :-
    Y_bottom is Y - 1,
    player_board(X, Y_bottom).
mark_possible_pit_bottom(X, Y) :-
    Y_bottom is Y - 1,
    board(X, Y_bottom),
    (player_possible_pit(X, Y_bottom); assert(player_possible_pit(X, Y_bottom))).
mark_possible_pit_bottom(_, _).

mark_possible_pit(X, Y) :-
    mark_possible_pit_top(X, Y),
    mark_possible_pit_left(X, Y),
    mark_possible_pit_bottom(X, Y),
    mark_possible_pit_right(X, Y), !.

mark_safe(X, Y) :-
    board(X, Y),
    (player_safe(X, Y); assert(player_safe(X, Y))), !.
mark_safe(_, _).

mark_spot(X, Y) :-
    player_board(X, Y).
mark_spot(X, Y) :-
    board(X, Y), 
    assertz(player_board(X, Y)), 
    assertz(player_safe(X, Y)),
    (retract(player_possible_pit(X, Y)); true),
    (retract(player_possible_wumpus(X, Y)); true), fail.
mark_spot(X, Y) :-
    smelly(X, Y),
    assertz(player_smelly(X, Y)), 
    mark_possible_wumpus(X, Y), fail.
mark_spot(X, Y) :-
    breezy(X, Y),
    assertz(player_breezy(X, Y)), 
    mark_possible_pit(X, Y), fail.
mark_spot(X, Y) :-
    pit(X, Y),
    assertz(player_pit(X, Y)), 
    retract(player_safe(X, Y)), 
    retract(player_possible_pit(X, Y)), fail.
mark_spot(X, Y) :- 
    wumpus(X, Y),
    assertz(player_wumpus(X, Y)), 
    retract(player_safe(X, Y)), 
    retract(player_possible_wumpus(X, Y)), fail.
mark_spot(X, Y) :-
    treasure(X, Y),
    assertz(player_treasure(X, Y)), fail.
mark_spot(X, Y) :-
    \+ player_smelly(X, Y),
    \+ player_breezy(X, Y),
    \+ player_pit(X, Y),
    \+ player_wumpus(X, Y),
    X_left is X - 1,
    mark_safe(X_left, Y),
    X_right is X + 1,
    mark_safe(X_right, Y),
    Y_top is Y + 1,
    mark_safe(X, Y_top),
    Y_bottom is Y - 1,
    mark_safe(X, Y_bottom), fail.
mark_spot(_, _).

deduct_pits :-
    player_possible_pit(X, Y),
    X_left is X - 1,
    X_right is X + 1,
    Y_top is Y + 1,
    Y_bottom is Y - 1,
    (
        board(X_left, Y), 
            player_board(X_left, Y); 
        \+ board(X_left, Y)
    ),
    (
        board(X_right, Y), 
            player_board(X_right, Y); 
        \+ board(X_right, Y)
    ),
    (
        board(X, Y_top), 
            player_board(X, Y_top); 
        \+ board(X, Y_top)
    ), 
    (
        board(X, Y_bottom), 
            player_board(X, Y_bottom); 
        \+ board(X, Y_bottom)
    ),
    (\+ player_pit(X, Y), assertz(player_pit(X, Y)); true),
    (retract(player_possible_pit(X, Y)); true),
    (retract(player_possible_wumpus(X, Y)); true),
    (retract(player_safe(X, Y)); true),
    fail.
deduct_pits.

deduct_wumpus :-
    player_possible_wumpus(X, Y),
    X_left is X - 1,
    X_right is X + 1,
    Y_top is Y + 1,
    Y_bottom is Y - 1,
    (
        board(X_left, Y), 
            player_board(X_left, Y); 
        \+ board(X_left, Y)
    ),
    (
        board(X_right, Y), 
            player_board(X_right, Y); 
        \+ board(X_right, Y)
    ),
    (
        board(X, Y_top), 
            player_board(X, Y_top); 
        \+ board(X, Y_top)
    ), 
    (
        board(X, Y_bottom), 
            player_board(X, Y_bottom); 
        \+ board(X, Y_bottom)
    ),
    (\+ player_wumpus(X, Y), assertz(player_wumpus(X, Y)); true),
    (retract(player_possible_pit(X, Y)); true),
    (retract(player_possible_wumpus(X, Y)); true),
    (retract(player_safe(X, Y)); true),
    fail.
deduct_wumpus.

mark_surroundings :-
    player(X, Y),
    mark_spot(X, Y),
    deduct_pits,
    deduct_wumpus, !.

print_player_cell(X, Y) :-
    (player_board(X, Y); player_pit(X, Y); player_wumpus(X, Y)),
    print_cell(X, Y), !.
print_player_cell(X, Y) :-
    (player_possible_pit(X, Y), player_possible_wumpus(X, Y), write('^');
    player_possible_pit(X, Y), write('o');
    player_possible_wumpus(X, Y), write('m')), !.
print_player_cell(X, Y) :-
    player_safe(X, Y), write(' '), !.
print_player_cell(_, _) :-
    write('?').

print_player_board(X, 1, X) :- nl, !.
print_player_board(X_Max, Y, X_Max) :-
    board(1, Y),
    nl,
    New_Y is Y - 1,
    print_player_board(1, New_Y, X_Max), !.
print_player_board(X, Y, X_Max) :-
    board(X, Y),
    print_player_cell(X, Y), 
    New_X is X + 1,
    print_player_board(New_X, Y, X_Max), !.

print_player_board :-
    size(Max_X, Max_Y),
    Max_X_Inc is Max_X + 1,
    print_player_board(1, Max_Y, Max_X_Inc).

safe(X, Y) :-
    hard_safe(X, Y),
    \+ player_possible_pit(X, Y),
    \+ player_possible_wumpus(X, Y).

hard_safe(X, Y) :-
    player_safe(X, Y).
hard_safe(X, Y) :-
    board(X, Y),
    \+ player_pit(X, Y),
    \+ player_wumpus(X, Y).

:-dynamic(is_safe).
no_undiscovered_safe_position :-
    retractall(is_safe),
    player_safe(X, Y),
    \+ player_board(X, Y),
    retractall(is_safe), assert(is_safe), fail.
no_undiscovered_safe_position :-
    \+ retract(is_safe).

next_move(up) :-
    player(X, Y),
    Y_top is Y + 1,
    safe(X, Y_top),
    \+ player_board(X, Y_top), !.
next_move(left) :-
    player(X, Y),
    X_left is X - 1,
    safe(X_left, Y),
    \+ player_board(X_left, Y), !.
next_move(down) :-
    player(X, Y),
    Y_bottom is Y - 1,
    safe(X, Y_bottom),
    \+ player_board(X, Y_bottom), !.
next_move(right) :-
    player(X, Y),
    X_right is X + 1,
    safe(X_right, Y),
    \+ player_board(X_right, Y), !.

next_move(up) :-
    no_undiscovered_safe_position,
    player(X, Y),
    Y_top is Y + 1,
    hard_safe(X, Y_top), !.
next_move(left) :-
    no_undiscovered_safe_position,
    player(X, Y),
    X_left is X - 1,
    hard_safe(X_left, Y), !.
next_move(down) :-
    no_undiscovered_safe_position,
    player(X, Y),
    Y_bottom is Y - 1,
    hard_safe(X, Y_bottom), !.
next_move(right) :-
    no_undiscovered_safe_position,
    player(X, Y),
    X_right is X + 1,
    hard_safe(X_right, Y), !.

next_move(up) :-
    player(X, Y),
    Y_top is Y + 1,
    safe(X, Y_top), !.
next_move(left) :-
    player(X, Y),
    X_left is X - 1,
    safe(X_left, Y), !.
next_move(down) :-
    player(X, Y),
    Y_bottom is Y - 1,
    safe(X, Y_bottom), !.
next_move(right) :-
    player(X, Y),
    X_right is X + 1,
    safe(X_right, Y), !.

next_move(up) :-
    player(X, Y),
    Y_top is Y + 1,
    hard_safe(X, Y_top), !.
next_move(left) :-
    player(X, Y),
    X_left is X - 1,
    hard_safe(X_left, Y), !.
next_move(down) :-
    player(X, Y),
    Y_bottom is Y - 1,
    hard_safe(X, Y_bottom), !.
next_move(right) :-
    player(X, Y),
    X_right is X + 1,
    hard_safe(X_right, Y), !.

move(up) :- move(top).
move(top) :-
    player(alive),
    retract(player(X, Y)),
    Y_top is Y + 1,
    assertz(player(X, Y_top)),
    mark_surroundings,
    hard_safe(X, Y_top), !.
move(top) :-
    retract(player(alive)),
    assertz(player(dead)).

move(right) :-
    player(alive),
    retract(player(X, Y)),
    X_right is X + 1,
    assertz(player(X_right, Y)),
    mark_surroundings,
    hard_safe(X_right, Y), !.
move(right) :-
    retract(player(alive)),
    assertz(player(dead)).

move(down) :- move(bottom).
move(bottom) :-
    player(alive),
    retract(player(X, Y)),
    Y_bottom is Y - 1,
    assertz(player(X, Y_bottom)),
    mark_surroundings,
    hard_safe(X, Y_bottom), !.
move(bottom) :-
    retract(player(alive)),
    assertz(player(dead)).

move(left) :-
    player(alive),
    retract(player(X, Y)),
    X_left is X - 1,
    assertz(player(X_left, Y)),
    mark_surroundings,
    hard_safe(X_left, Y), !.
move(left) :-
    retract(player(alive)),
    assertz(player(dead)).

max_turns(9).
:-  dynamic(turn/1).
game :-
    make_board,
    mark_surroundings,
    assert(turn(1)),
    max_turns(Turn_limit),
    write('Game Board'), nl,
    print_board,
    repeat,
    retract(turn(Nr)),
    write('Turn '), write(Nr), nl,
    New_nr is Nr + 1,
    assert(turn(New_nr)),
    write('Player knowledge'), nl,
    print_player_board,
    write('Player makes a move to '),
    next_move(Move),
    move(Move),
    write(Move), nl,
    (player(dead), write('Player died'), nl; 
    player(X, Y), treasure(X, Y), write('Player got treasure'), nl;
    Nr = Turn_limit, write('Player ran out of turns'), nl),
    write('Player final knowledge'), nl,
    print_player_board, !.
