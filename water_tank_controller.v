module water_tank_controller (
    input  wire clk,
    input  wire rst,
    input  wire low_level,
    input  wire high_level,
    output reg  pump_on
);

    localparam IDLE    = 1'b0;
    localparam FILLING = 1'b1;

    reg state;

    always @(posedge clk) begin
        if (rst) begin
            state   <= IDLE;
            pump_on <= 1'b0;
        end else begin
            case (state)
                IDLE: begin
                    pump_on <= 1'b0;

                    if (!low_level)
                        state <= FILLING;
                end

                FILLING: begin
                    if (high_level) begin
                        pump_on <= 1'b0;
                        state   <= IDLE;
                    end else begin
                        pump_on <= 1'b1;
                    end
                end

                default: begin
                    state   <= IDLE;
                    pump_on <= 1'b0;
                end
            endcase
        end
    end

endmodule
