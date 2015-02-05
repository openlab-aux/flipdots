/*
* Copyright (c) 2013 Franz Nord
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 3
* of the License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
*
* For more information on the GPL, please go to:
* http://www.gnu.org/copyleft/gpl.html
*/

#ifndef FLIPDOT_H
#define FLIPDOT_H

#include <stdint.h>

enum sreg {
	ROW,
	COL
};

typedef struct {
    int data_col;
    int data_row;
    int strobe;
    int oe_white;
    int oe_black;
    int clk_col;
    int clk_row;
} flipdot_pinning;

#define FLIP_DELAY_BLACK 3000			/* us */
#define FLIP_DELAY_WHITE 1500			/* us */
#define STROBE_DELAY 1			/* us */

#define MODULE_COUNT 4

#define MODULE_ROWS 16
#define MODULE_COLS 20

#define MODULE_PIXEL_COUNT (MODULE_ROWS*MODULE_COLS)
#define MODULE_BYTE_COUNT  (MODULE_PIXEL_COUNT/8)

#define ROW_GAP 4

#define DISP_COLS   MODULE_COUNT*MODULE_COLS
#define DISP_ROWS   MODULE_ROWS

#define DISP_PIXEL_COUNT (DISP_ROWS*DISP_COLS)
#define DISP_BYTE_COUNT  (DISP_PIXEL_COUNT/8)


void flipdot_init(void);
void flipdot_deinit(void);
void flipdot_data(uint8_t *frames, uint16_t size);
#endif /* FLIPDOT_H */
